from flask import Flask, request, make_response, jsonify, abort
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods = [ 'GET', 'POST' ] )
def messages():

    if request.method == 'GET' :
        messages = [ message.to_dict() for message in Message.query.order_by( Message.created_at.asc() ).all() ]

        return make_response( jsonify( messages ), 200 )
        
    elif request.method == 'POST' :
        new_message = Message(
            body = request.get_json()['body'],
            username = request.get_json()['username']
        )
        db.session.add( new_message )
        db.session.commit()

        return make_response( jsonify( new_message.to_dict() ), 201 )


@app.route('/messages/<int:id>', methods = [ 'PATCH', 'DELETE' ] )
def messages_by_id(id):
    message = Message.query.filter( Message.id == id ).first()
    if message :
        if request.method == 'DELETE' :
            db.session.delete( message )
            db.session.commit()

            return make_response( '', 204 )
        
        elif request.method == 'PATCH' :
            for key in request.get_json() :
                setattr( message, key, request.get_json()[ key ] )
            db.session.add( message )
            db.session.commit()
            
            return make_response( jsonify( message.to_dict() ), 200 )
            
    else :
        return make_response( 'Message not found.', 404 )


if __name__ == '__main__':
    app.run(port=5555, debug=True)
