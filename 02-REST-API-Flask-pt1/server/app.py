#!/usr/bin/env python3

# 📚 Review With Students:
    # API Fundamentals
    # MVC Architecture and Patterns / Best Practices
    # RESTful Routing
    # Serialization
    # Postman

# Set Up:
    # In Terminal, `cd` into `server` and run the following:
        # export FLASK_APP=app.py
        # export FLASK_RUN_PORT=5000
        # flask db init
        # flask db revision --autogenerate -m 'Create tables' 
        # flask db upgrade 
        # python seed.py

# Restful

# | HTTP Verb 	|       Path       	| Description        	|
# |-----------	|:----------------:	|--------------------	|
# | GET       	|   /productions   	| READ all resources 	|
# | GET       	| /productions/:id 	| READ one resource   	|
# | POST      	|   /productions   	| CREATE one resource 	|
# | PATCH/PUT 	| /productions/:id 	| UPDATE one resource	|
# | DELETE    	| /productions/:id 	| DESTROY one resource 	|



from flask import Flask, request, make_response, jsonify, abort
from flask_migrate import Migrate

# 1. ✅ Import `Api` and `Resource` from `flask_restful`
    # ❓ What do these two classes do at a higher level?
from flask_restful import Api, Resource
from models import db, Production, CastMember


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Note: `app.json.compact = False` 
# configures JSON responses to print on indented lines
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# 2. ✅ Initialize the Api
api = Api(app)


# 3. ✅ Create a Production class that inherits from Resource
# This resource is for the '/productions' end point.
class Productions(Resource):
# 4. ✅ Create a GET (All) Route
    def get(self):
        productions = Production.query.all()
        # production_response = [{
        #     "title": production.title, 
        #     "genre": production.genre,
        #     "director": production.director,
        #     "description":production.description,
        #     "image": production.image,
        #     "budget":production.budget,
        #     "ongoing":production.ongoing
        # } for production in productions]
        
        # for every production, convert them to a dict, and save in array.
        production_list = [production.to_dict() for production in productions]

        response = make_response(
            production_list,
            200
        )

        return response
    
    def post(self):
        request_json = request.get_json()

        new_production = Production(
            title = request_json['title'],
            genre=request_json['genre'],
            budget=request_json['budget'],
            image=request_json['image'],
            director=request_json['director'],
            description=request_json['description'],
            ongoing=request_json['ongoing']
        )

        db.session.add(new_production)
        db.session.commit()

        response = make_response(
            new_production.to_dict(),
            201
            )
        return response


#(this is step 12)
api.add_resource(Productions, '/productions')

    # 4.1 Make a `get` method that takes `self` as a param.
    # 4.2 Create a `productions` array.
    # 4.3 Make a query for all productions. For each `production`, create a dictionary 
    # containing all attributes before appending to the `productions` array.
    # 4.4 Create a `response` variable and set it to: 
    #  #make_response(
    #       jsonify(productions),
    #       200
    #  )
    # 4.5 Return `response`.
    # 4.6 After building the route, run the server and test in the browser.
  
# 5. ✅ Serialization
    # This is great, but there's a cleaner way to do this! Serialization will allow us to easily add our 
    # associations as well.
    # Navigate to `models.py` for Steps 6 - 9.
    
    # done!

# 10. ✅ Use our serializer to format our response to be cleaner
    # 10.1 Query all of the productions, convert them to a dictionary with `to_dict` before setting them to a list.
    # 10.2 Invoke `make_response`, pass it the production list along with a status of 200. Set `make_response` to a 
    # `response` variable.
    # 10.3 Return the `response` variable.
    # 10.4 After building the route, run the server and test your results in Thunder Client :)!
 
# 11. ✅ Create a POST Route
    # Prepare a POST request in Postman. Under the `Body` tab, select `form-data` and fill out the body 
    # of a production request. 
    
    # Create the POST route 
    # 📚 Review With Students: request object
    
    # 11.1 Create a `post` method and pass it `self`.
    # 11.2 Create a new production from the `request.form` object.
    # 11.3 Add and commit the new production.
    # 11.4 Convert the new production to a dictionary with `to_dict`
    # 11.5 Set `make_response` to a `response` variable and pass it the new production along with a status of 201.
    # 11.6 Test the route in Postman.

   
# 12. ✅ Add the new route to our api with `api.add_resource`
# we did this earlier, and we also tested it with Thunder Client!

# 13. ✅ Create a GET (One) route
    # 13.1 Build a class called `ProductionByID` that inherits from `Resource`.
    # 13.2 Create a `get` method and pass it the id along with `self`. (This is how we will gain access to 
    # the id from our request)
class ProductionById(Resource):
    def get(self, id):
        
        # Make a query for our production by the `id'.
        production = Production.query.filter_by(id=id).first()

        if not production:
            abort(404, 'The Production you were looking for was not found!')

        production_dict = production.to_dict()
        
        # Build a `response` to send to the browser.
        response = make_response(
            production_dict,
            200
        )

        return response
    
    def patch(self, id):
        # Make a query for our production by the `id'.
        production = Production.query.filter_by(id=id).first()

        if not production:
            abort(404, 'The Production you were looking for was not found!')

        request_json = request.get_json()
        # For every key given to us by the request, in our request json
        for key in request_json:
            # Let's set that attribute on production, with the new value
            setattr(production,key,request_json[key])
        #for example
            #setattr(production,'title', request_json['title'] -> "May 25 Lecture")

        # now production has been patched successfully!

        production_dict = production.to_dict()

        # Build a `response` to send to the browser.
        response = make_response(
            production_dict,
            200
        )
        return response
    
    def delete(self, id):
        production = Production.query.filter_by(id=id).first()
        if not production:
            abort(404, 'The Production you were looking for was not found!')

        db.session.delete(production)
        db.session.commit()

        response = make_response ('', 204)

        return response

# This is saying we are defining an endpoint with the resource productionById
api.add_resource(ProductionById, '/productions/<int:id>')

# 14. ✅ Add the new route to our api with `api.add_resource`

# Note: If you'd like to run the application as a script instead of using `flask run`, uncomment the line below 
# and run `python app.py`
if __name__ == '__main__':
    app.run(port=5555, debug=True)