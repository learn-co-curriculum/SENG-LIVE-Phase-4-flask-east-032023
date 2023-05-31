#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [ {
        "id":  bakery.id,
        "name": bakery.name,
        'created_at': bakery.created_at
    } for bakery in Bakery.query.all() ]
    return make_response( jsonify( bakeries ), 200 )

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter( Bakery.id == id ).first()
    if bakery :
        return make_response( jsonify( bakery.to_dict() ), 200 )
    else : return make_response( "Could not find that bakery.", 404 )

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = [ {
        "id": bg.id,
        "name": bg.name,
        "price": bg.price,
        'created_at': bg.created_at
    } for bg in BakedGood.query.order_by( BakedGood.price.desc() ).all() ]
    return make_response( jsonify( baked_goods ), 200 )

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    bg = BakedGood.query.order_by( BakedGood.price.desc() ).first()
    baked_good = {
        "id": bg.id,
        "name": bg.name,
        "price": bg.price,
        'created_at': bg.created_at
    }
    return make_response( jsonify( baked_good ), 200 )

if __name__ == '__main__':
    app.run(port=5555, debug=True)
