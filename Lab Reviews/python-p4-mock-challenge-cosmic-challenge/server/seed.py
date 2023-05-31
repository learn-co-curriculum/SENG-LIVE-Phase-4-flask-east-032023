from random import randint, choice as rc

from faker import Faker

from app import app
from models import db, Planet, Scientist, Mission

fake = Faker()

if __name__ == '__main__':

    with app.app_context():
        print("Clearing db...")
        Planet.query.delete()
        Scientist.query.delete()
        Mission.query.delete()

        p1 = Planet(
            name = 'Mars',
            distance_from_earth = '74924739',
            nearest_star = 'Nebula',
            image = 'faskfdjakldj.jpg'
        )
        p2 = Planet(
            name = 'Jupiter',
            distance_from_earth = 'far away',
            nearest_star = 'Sun',
            image = 'djfa;dfja;.jpg'
        )

        p3 = Planet(
            name = 'Pluto',
            distance_from_earth = 'even farther away',
            nearest_star = 'Comet',
            image = 'fdafdsjfasfjasl.jpg'
        )

        db.session.add_all( [p1, p3, p2] )
        db.session.commit()

        s1 = Scientist(
            name = fake.name(),
            field_of_study = fake.city(),
            avatar = fake.city_prefix(),
        )
        s2 = Scientist(
            name = fake.name(),
            field_of_study = fake.city(),
            avatar = fake.city_prefix(),
        )
        s3 = Scientist(
            name = fake.name(),
            field_of_study = fake.city(),
            avatar = fake.city_prefix(),
        )
        
        db.session.add_all( [s1, s2, s3] )
        db.session.commit()

        m1 = Mission(
            name = "Apollo 13",
            scientist_id = s1.id,
            planet_id = p1.id
        )
        m2 = Mission(
            name = "Apollo 11",
            scientist_id = s2.id,
            planet_id = p3.id
        )
        m3 = Mission(
            name = "Apollo 13",
            scientist_id = s3.id,
            planet_id = p1.id
        )
        m4 = Mission(
            name = "Apollo 10",
            scientist_id = s2.id,
            planet_id = p2.id
        )
        db.session.add_all( [m1, m2, m3, m4] )
        db.session.commit()

        print("Done seeding!")
