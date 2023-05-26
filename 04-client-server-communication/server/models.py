# 📚 Review With Students:
    # Validations and Invalid Data

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from flask import abort

# 1.✅ Import validates from sqlalchemy.orm
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Production(db.Model, SerializerMixin):
    __tablename__ = 'productions'

    id = db.Column(db.Integer, primary_key=True)
     

    title = db.Column(db.String)
    genre = db.Column(db.String)
    budget = db.Column(db.Float)
    image = db.Column(db.String)
    director = db.Column(db.String)
    description = db.Column(db.String)
    ongoing = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    cast_members = db.relationship('CastMember', backref='production')
        
    serialize_rules = ('-cast_members.production',)



# 3.✅ Use the "validates" decorator to create a validation for images
    @validates( 'image' )
    def validate_image ( self, key, image_url ) :
        if type( image_url ) is str and image_url and '.jpg' in image_url :
            return image_url
        else :
            abort( 422, 'Image URL must be a string and be a .jpg path.' )
            # raise ValueError( 'Image URL must be a string and be a .jpg path.' )
 
    @validates( 'budget' )
    def validate_budget ( self, key, budget ) :
        if type( budget ) is int and budget > 0 :
            return budget
        else :
            abort( 422, 'Budget must be an number greater than 0.' )

    def __repr__(self):
        return f'<Production Title:{self.title}, Genre:{self.genre}, Budget:{self.budget}, Image:{self.image}, Director:{self.director},ongoing:{self.ongoing}>'

class CastMember(db.Model, SerializerMixin):
    __tablename__ = 'cast_members'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    # 2.✅ set role nullable to false
    role = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    production_id = db.Column(db.Integer, db.ForeignKey('productions.id'))
    
    serialize_rules = ('-production.cast_members',)

    @validates( 'name' )
    def validate_name ( self, key, name ) :
        if type( name ) is str and name :
            return name
        else : 
            abort( 422, 'Name must be a string and more than 0 characters.' )
            # raise ValueError( 'Name must be a string and more than 0 characters.' )

    @validates( 'role' )
    def validate_role ( self, key, role ) :
        if type( role ) is str and role :
            return role
        else : 
            abort( 422, 'Role must be a string and more than 0 characters.' )
            # raise ValueError( 'Role must be a string and more than 0 characters. ' )

    def __repr__(self):
        return f'<Production Name:{self.name}, Role:{self.role}'

