#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Planet, Scientist, Mission

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return ''

@app.route( '/scientists', methods = [ 'GET', 'POST' ] )
def scientists ( ) :

    if request.method == 'GET' :
        scientists = [ scientist_to_dict( sc ) for sc in Scientist.query.all() ]

        return make_response( jsonify( scientists ), 200 )
    
    elif request.method == 'POST' :
        new_scientist = Scientist(
            name = request.get_json()['name'],
            avatar = request.get_json()['avatar'],
            field_of_study = request.get_json()['field_of_study']
        )
        db.session.add( new_scientist )
        db.session.commit()
        
        return make_response( jsonify( scientist_to_dict( new_scientist ) ), 201 )


@app.route( '/scientists/<int:id>', methods = [ 'GET', 'PATCH', 'DELETE' ] )
def scientist ( id ) :
    scientist = Scientist.query.filter( Scientist.id == id ).first()

    if scientist :
    
        if request.method == 'GET' :

            scientist_dict = scientist_to_dict( scientist )
            scientist_dict['planets'] = [ planet_to_dict( planet ) for planet in scientist.planets ]
            return make_response( jsonify( scientist_dict ), 200 )
    
        if request.method == 'PATCH' :
            for attr in request.get_json() :
                setattr( scientist, attr, request.get_json()[ attr ] )
            
            db.session.add( scientist )
            db.session.commit()

            return make_response( jsonify( scientist_to_dict( scientist ) ), 200 )
    
        if request.method == 'DELETE' :
            db.session.delete( scientist )
            db.session.commit()
            
            return make_response( '', 204 )
    else :
        return make_response( "Scientist not found.", 404 )
    

@app.route( '/planets' )
def planets ( ) :
    planets = [ planet_to_dict( planet ) for planet in Planet.query.all() ]
    return make_response( jsonify( planets ), 200 )

@app.route( '/missions', methods = ['POST'] )
def missions ( ) :
    if request.method == 'POST' :
        new_mission = Mission(
            name = request.get_json()['name'],
            scientist_id = request.get_json()['scientist_id'],
            planet_id = request.get_json()['planet_id']
        )
        db.session.add( new_mission )
        db.session.commit()
        
        return make_response( jsonify( planet_to_dict( new_mission.planet ) ), 201 )


def scientist_to_dict ( sc ) :
    return {
            "id": sc.id,
            "name": sc.name,
            'field_of_study': sc.field_of_study,
            'avatar': sc.avatar
        }

def planet_to_dict( planet ) :
    return {
        "id": planet.id,
        "name": planet.name,
        "distance_from_earth": planet.distance_from_earth,
        "nearest_star": planet.nearest_star,
        "image": planet.image
    }

if __name__ == '__main__':
    app.run(port=5555, debug=True)
