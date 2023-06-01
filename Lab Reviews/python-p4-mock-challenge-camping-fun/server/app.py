#!/usr/bin/env python3

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'instance/app.db')}")

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Activity, Camper, Signup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return ''

@app.route( '/campers', methods = [ 'GET', 'POST' ] )
def campers ( ) :

    if request.method == 'GET' :
        campers = Camper.query.all()
        campers_to_dicts = [ camper.camper_to_dict() for camper in campers ]
        
        return make_response( jsonify( campers_to_dicts ), 200 )
    
    elif request.method == 'POST' :
        rq = request.get_json()
        new_camper = Camper(
            name = rq[ 'name' ],
            age = rq[ 'age' ]
        )
        db.session.add( new_camper )
        db.session.commit()

        return make_response( jsonify( new_camper.camper_to_dict() ), 201 )


@app.route( '/campers/<int:id>' )
def camper ( id ) :
    camper = Camper.find( id )
    if camper :
        camper_to_dict = camper.camper_to_dict()
        camper_to_dict['activities'] = [ activity.activity_to_dict() for activity in camper.activities ]

        return make_response( jsonify( camper_to_dict ), 200 )
    
    else :
        return make_response( 'Camper not found.', 404 )
    

@app.route( '/activities' )
def activities ( ) :
    activities = Activity.query.all()
    activities_to_dicts = [ activity.activity_to_dict() for activity in activities ]

    return make_response( jsonify( activities_to_dicts ), 200 )


@app.route( '/activities/<int:id>', methods = [ 'DELETE' ] )
def activity ( id ) :
    activity = Activity.find( id )
    if activity :
        for signup in activity.signups :
            db.session.delete( signup )

        db.session.delete( activity )
        db.session.commit()

        return make_response( '', 204 )
    
    else : 
        return make_response( 'Activity not found.', 404 )
    

@app.route( '/signups', methods = [ 'POST' ] )
def signups ( ) :
    if request.method == 'POST' :
        rq = request.get_json()
        new_signup = Signup(
            time = rq[ 'time' ],
            camper_id = rq[ 'camper_id' ],
            activity_id = rq[ 'activity_id' ]
        )
        db.session.add( new_signup )
        db.session.commit()

        return make_response( jsonify( new_signup.activity.activity_to_dict() ), 201 )


if __name__ == '__main__':
    app.run(port=5555, debug=True)
