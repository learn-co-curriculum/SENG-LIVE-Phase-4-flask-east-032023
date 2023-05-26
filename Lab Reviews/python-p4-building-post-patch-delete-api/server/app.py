#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

@app.route('/games', methods = [ 'GET', 'POST' ] )
def games():


    games = []
    for game in Game.query.all():
        game_dict = {
            "title": game.title,
            "genre": game.genre,
            "platform": game.platform,
            "price": game.price,
            "id": game.id
        }
        games.append(game_dict)

    response = make_response(
        games,
        200
    )

    return response

@app.route('/games/<int:id>')
def game_by_id(id):
    game = Game.query.filter(Game.id == id).first()
    
    game_dict = game.to_dict()

    response = make_response(
        game_dict,
        200
    )

    return response

@app.route('/reviews', methods = [ 'GET', 'POST' ] )
def reviews():

    body = None
    status_code = None

    if request.method == "GET" :
        reviews = []
        for review in Review.query.all():
            review_dict = review.to_dict()
            reviews.append(review_dict)
        body = reviews
        status_code = 200

    elif request.method == 'POST' :
        # print( request.get_json()['score'] )
        review_data = request.get_json()
        new_review = Review(
            comment = review_data['comment'],
            score = review_data['score'],
            user_id = review_data['user_id'],
            game_id = review_data['game_id']
        )
        db.session.add( new_review )
        db.session.commit()
        body = new_review.to_dict()
        status_code = 201

    return make_response( jsonify( body ), status_code )


@app.route( '/reviews/<int:id>', methods = [ 'GET', 'DELETE', 'PATCH' ] )
def review ( id ) :
    review = Review.query.filter( Review.id == id ).first()
    if review :
        body = None
        status_code = None

        if request.method == 'GET' :
            body = review.to_dict()
            status_code = 200

        elif request.method == 'DELETE' :
            db.session.delete( review )
            db.session.commit()
            status_code = 204

        elif request.method == 'PATCH' :
            updated_review = request.get_json()
            for key in updated_review :
                setattr( review, key, updated_review[ key ] )
            db.session.add( review )
            db.session.commit()
            body = review.to_dict()
            status_code = 200
        
        return make_response( jsonify( body ) , status_code )
    else :
        abort( 404, 'Could not find that review.' )


@app.route('/users')
def users():

    users = []
    for user in User.query.all():
        user_dict = user.to_dict()
        users.append(user_dict)

    response = make_response(
        users,
        200
    )

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
