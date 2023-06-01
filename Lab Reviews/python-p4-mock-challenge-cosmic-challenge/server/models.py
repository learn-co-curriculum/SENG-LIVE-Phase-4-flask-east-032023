from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from flask import abort

convention = {
  "ix": "ix_%(column_0_label)s",
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)

class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets'

    # serialize_rules = ( '-scientists.planet', )
    serialize_rules = ( '-missions.planet', '-scientists.planets' )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    distance_from_earth = db.Column(db.String)
    nearest_star = db.Column(db.String)
    image = db.Column(db.String)
    created_at = db.Column( db.DateTime, server_default = db.func.now() )
    updated_at = db.Column( db.DateTime, onupdate = db.func.now() )

    missions = db.relationship( 'Mission', backref = 'planet' )
    scientists = association_proxy( 'missions', 'scientist' )

    def __repr__(self):
        return f'<Planet {self.id}: {self.name}>'

class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists'

    # serialize_rules = ( '-planets.scientist', )
    serialize_rules = ( '-missions.scientist', '-planets.scientists' )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    field_of_study = db.Column(db.String)
    avatar = db.Column(db.String)
    created_at = db.Column( db.DateTime, server_default = db.func.now() )
    updated_at = db.Column( db.DateTime, onupdate = db.func.now() )

    missions = db.relationship( 'Mission', backref = 'scientist' )
    planets = association_proxy( 'missions', 'planet' )


    @validates( 'field_of_study' )
    def validate_field ( self, attr, field ) :
        if type( field ) is str and field :
            return field
        else :
            abort( 422, 'Scientist must have a field of study that is a string and is more than 0 characters.' )

    @validates( 'name' )
    def validate_name ( self, attr, name ) :
        sc = Scientist.query.filter( Scientist.name.like( f'%{ name }%' ) ).first()
        print( sc )
        if type( name ) is str and name and sc == None:
            return name
        else :
            abort( 422, 'Name must be a string and unique.' )

    def __repr__(self):
        return f'<Scientist {self.id}: {self.name}>'

class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions'

    # serialize_rules = ( '-mission.scientist, -mission.planet' )
    serialize_rules = ( '-scientist.missions', '-planet.missions' )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column( db.String )
    created_at = db.Column( db.DateTime, server_default = db.func.now() )
    updated_at = db.Column( db.DateTime, onupdate = db.func.now() )

    scientist_id = db.Column( db.Integer, db.ForeignKey( 'scientists.id' ) )
    planet_id = db.Column( db.Integer, db.ForeignKey( 'planets.id' ) )

    @validates( 'name' )
    def validate_name ( self, attr, name ) :
        if type( name ) is str and name :
            return name
        else : abort( 422, 'Name must be a string and more than 0 characters.' )
    
    @validates( 'planet_id' )
    def validate_planet ( self, attr, id ) :
        if type( id ) is int and id > 0 :
            return id
        else : abort( 422, 'Planet id must be an integer greater than 0.' )

    @validates( 'scientist_id' )
    def validates_scientist ( self, attr, id ) :
        mission = Mission.query.filter( Mission.name == self.name, Mission.scientist_id == id ).first()
        if type( id ) is int and id > 0 and mission == None :
            return id
        else : abort( 422, 'Scientist id must be a number and greater than 0.' )

    def __repr__(self):
        return f'<Mission {self.id}: {self.name}>'

# add any models you may need. 