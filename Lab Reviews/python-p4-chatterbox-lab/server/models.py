from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from flask import abort

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column( db.String )
    username = db.Column( db.String )
    created_at = db.Column( db.DateTime, server_default=db.func.now() )
    updated_at = db.Column( db.DateTime, onupdate=db.func.now() )

    @validates( 'username' )
    def validate_username ( self, attr, username ) :
        if type( username ) is str and username :
            return username
        else :
            abort( 422, 'Username must be a string and cannot be blank.' )

    @validates( 'body' )
    def validate_body ( self, attr, body ) :
        if type( body ) is str and body :
            return body
        else :
            abort( 422, 'Body of message must be a string and cannot be blank.' )


