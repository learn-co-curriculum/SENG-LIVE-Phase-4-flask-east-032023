# 📚 Review With Students:
    # Validations and Invalid Data

from flask_sqlalchemy import SQLAlchemy
from flask import abort
from sqlalchemy_serializer import SerializerMixin

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
    def validate_image_url ( self, key, image_url ) :
        if '.jpg' in image_url or '.gif' in image_url or '.jpeg' in image_url :
            return image_url
        else : abort( 422, 'Image must have a valid url.' )

    def __repr__(self):
        return f'<Production Title:{self.title}, Genre:{self.genre}, Budget:{self.budget}, Image:{self.image}, Director:{self.director},ongoing:{self.ongoing}>'

class CastMember(db.Model, SerializerMixin):
    __tablename__ = 'cast_members'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    # 2.✅ set role nullable to false
    role = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    production_id = db.Column(db.Integer, db.ForeignKey('productions.id'))
    
    serialize_rules = ('-production.cast_members',)

    @validates( 'name' )
    def validate_name ( self, key, name ) :
        if name and type( name ) is str :
            return name
        else : 
            abort( 422, 'Name must exist and not be an empty string.' )

    @validates( 'role' )
    def validate_role ( self, key, role ) :
        if role and type( role ) is str :
            return role
        else : abort( 422, 'Role must exist and not be an empty string.' )

    def __repr__(self):
        return f'<Production Name:{self.name}, Role:{self.role}'

