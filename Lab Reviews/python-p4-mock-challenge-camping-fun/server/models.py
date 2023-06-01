from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from flask import abort, make_response

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)

class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)
    created_at = db.Column( db.DateTime, server_default = db.func.now() )
    updated_at = db.Column( db.DateTime, onupdate = db.func.now() )

    serailize_rules = ( '-signups.activity', '-campers.activities' )

    signups = db.relationship( 'Signup', backref = 'activity' )
    campers = association_proxy( 'signups', 'camper' )

    def activity_to_dict ( self ) :
        return {
            'name': self.name,
            'id': self.id,
            'difficulty': self.difficulty
        }

    @classmethod
    def find ( cls, id ) :
        activity = Activity.query.filter( Activity.id == id ).first()
        return activity

    def __repr__(self):
        return f'<Activity {self.id}: {self.name}>'

class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)
    created_at = db.Column( db.DateTime, server_default = db.func.now() )
    updated_at = db.Column( db.DateTime, onupdate = db.func.now() )

    serialize_rules = ('-activities.campers', '-signups.camper')

    signups = db.relationship( 'Signup', backref = 'camper' )
    activities = association_proxy( 'signups', 'activity' )

    @classmethod
    def find ( cls, id ) :
        camper = Camper.query.filter( Camper.id == id ).first()
        return camper

    @validates( 'name' )
    def validate_name ( self, db_column, name ) :
        if type( name ) is str and name :
            return name
        else :
            abort( 422, "Name must be a string and more than 0 characters." )
    
    @validates( 'age' )
    def validate_age ( self, db_column, age ) :
        if type( age ) is int and 8 <= age <= 18 :
            return age
        else :
            abort( 422, "Age must be an integer between 8 and 18." )

    def camper_to_dict ( self ) :
        return {
            'name': self.name,
            'id': self.id,
            'age': self.age
        }

    def __repr__(self):
        return f'<Camper {self.id}: {self.name}>'
    
class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column( db.Integer )
    created_at = db.Column( db.DateTime, server_default = db.func.now() )
    updated_at = db.Column( db.DateTime, onupdate = db.func.now() )

    serialize_rules = ( '-camper.signups', '-activity.signups' )

    camper_id = db.Column( db.Integer, db.ForeignKey( 'campers.id' ) )
    activity_id = db.Column( db.Integer, db.ForeignKey( 'activities.id' ) )

    @validates( 'time' )
    def validate_time ( self, db_column, time ) :
        if type( time ) is int and 0 <= time <= 23 :
            return time
        else :
            abort( 422, "Time must be an integer between 0 and 23." )

    @validates( 'camper_id' )
    def validate_camper ( self, db_column, camper_id ) :
        camper = Camper.find( camper_id )
        if camper :
            return camper_id
        else :
            abort( 404, 'Camper not found.' )

    @validates( 'activity_id' )
    def validate_activity ( self, db_column, activity_id ) :
        activity = Activity.find( activity_id )
        if activity :
            return activity_id
        else :
            abort( 404, 'Activity not found.' )

    def __repr__(self):
        return f'<Signup {self.id}>'


# add any models you may need. 