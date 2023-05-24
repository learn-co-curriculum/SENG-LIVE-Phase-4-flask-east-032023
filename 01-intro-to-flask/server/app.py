#!/usr/bin/env python3

# 📚 Review With Students:
    # Request-Response Cycle
    # Web Servers and WSGI/Werkzeug

# 1. ✅ Navigate to `models.py`

# 2. ✅ Set Up Imports
from flask import Flask, jsonify, make_response, request, abort
from flask_migrate import Migrate

from models import db, Production

# 3. ✅ Initialize the App
  
    
    # Configure the database
    # ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    # ['SQLALCHEMY_TRACK_MODIFICATIONS'] = False`
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)    

 # 4. ✅ Migrate
# export FLASK_APP=app.py
# export FLASK_RUN_PORT=5555
# flask db init
# flask db revision --autogenerate -m 'Create tables productions'
# flask db upgrade
 # -- done! 

# 5. ✅ Navigate to `seed.py`
# -- seeding done!

# 12. ✅ Routes

# Let's define our home route!
@app.route('/')
def index():
    # code that does stuff
    html_code = '<h1>Hello World</h1>'
    return html_code

#Student Challenge: Create a route to '/image' that displays an image on the Browser
#/image
@app.route('/image')
def image():
    html_code = '<img src= "https://e7.pngegg.com/pngimages/476/159/png-clipart-pokemon-pikachu-pikachu-pokemon-games-pokemon-thumbnail.png">'
    return html_code

# 13. ✅ Run the server with `flask run` and verify your route in the browser at `http://localhost:5000/`
# - Done! It works!

# 14. ✅ Create a dynamic route (15 - Update this Dynamic Route)
@app.route('/productions/<string:title>')
def production (title):
    
    # find a `production` by its `title`
    production = Production.query.filter(Production.title == title).first()
    production_response = {
        "title": production.title, 
        "genre": production.genre,
        "director": production.director,
        "description":production.description,
        "image": production.image,
        "budget":production.budget,
        "ongoing":production.ongoing
    }
    response = make_response(
        jsonify(production_response),
        200
    )
    # send it to our browser
    return response

# 16.✅ Demo request context 
@app.route('/context')
def context():
    # import ipdb; ipdb.set_trace()
    # return f'<h1>Path{request.path} Host:{request.host}</h1>'
    
    # hypothetically, something wrong happens
    # so i run this abort command with Status Code 418
    abort(418)

# Note: If you'd like to run the application as a script instead of using `flask run`, uncomment the line below 
# and run `python app.py`
if __name__ == '__main__':
    app.run(port=5555, debug=True)
