"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planeta, Personaje, Favoritos
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)

# EndPoints
# GET: Todos los Usuarios


@app.route('/user', methods=['GET'])
def get_user():

    users = User.query.all()
    response_body = {
        "data": [user.serialize() for user in users]
    }

    return jsonify(response_body), 200


# GET: Todos los Personajes
@app.route('/people', methods=['GET'])
def get_people():
    personajes = Personaje.query.all()

    response_body = {
        "data": [personaje.serialize() for personaje in personajes]
    }

    return jsonify(response_body), 200

# GET: Un solo Personaje


@app.route('/people/<int:people_id>', methods=['GET'])
def get_singlePeople(people_id):

    singlePeople = Personaje.query.get_or_404(people_id)
    response_body = {
        "data": singlePeople.serialize()
    }

    return jsonify(response_body), 200


# GET: Todos los PLanetas
@app.route('/planets', methods=['GET'])
def get_planets():

    planetas = Planeta.query.all()
    response_body = {
        "data": [planeta.serialize() for planeta in planetas]
    }

    return jsonify(response_body), 200

# GET: Un solo planeta


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_singlePlanet(planet_id):

    singlePlaneta = Planeta.query.get_or_404(planet_id)
    response_body = {
        "data": singlePlaneta.serialize()
    }
    return jsonify(response_body), 200

# POST: planeta


@app.route('/planets', methods=['POST'])
def post_planet():

    data = request.json

    new_planeta = Planeta(
        name=data['name'],
        rotation_period=data['rotation_period'],
        diameter=data['diameter'],
        gravity=data['gravity'],
        orbital_period=data['orbital_period'],
        population=data['population'],
        climate=data['climate'],
        surface_water=data['surface_water'],
        terrain=data['terrain']
    )

    db.session.add(new_planeta)
    db.session.commit()

    response_body = {
        "data": new_planeta.serialize()
    }

    return jsonify(response_body), 201

# POST: Persona


@app.route('/people', methods=['POST'])
def post_people():

    data = request.json
    new_people = Personaje(
        name=data['name'],
        birth_year=data['birth_year'],
        eye_color=data['eye_color'],
        gender=data['gender'],
        hair_color=data['hair_color'],
        height=data['height'],
        mass=data['mass'],
        skin_color=data['skin_color'],
        species=data['species']
    )
    db.session.add(new_people)
    db.session.commit()

    response_body = {
        "data": new_people.serialize()
    }

    return jsonify(response_body), 201

# PUT: Persona
@app.route('/people/<int:people_id>', methods=['PUT'])
def put_people(people_id):

    people = Personaje.query.filter_by(id=people_id).first()

    if not people:
        return jsonify({
            "msg": "la persona no existe"
        }), 404

    data = request.json

    people.name=data.get('name', people.name)
    people.birth_year=data.get('birth_year', people.birth_year)
    people.eye_color=data.get('eye_color', people.eye_color)
    people.gender=data.get('gender', people.gender)
    people.hair_color=data.get('hair_color',  people.hair_color)
    people.height=data.get('height',  people.height)
    people.mass=data.get('mass', people.mass)
    people.skin_color=data.get('skin_color', people.skin_color)
    people.species=data.get('species', people.species)
    
    db.session.commit()

    response_body = {
        "data": people.serialize()
    }

    return jsonify(response_body), 200

# PUT: Planeta


@app.route('/planets/<int:planet_id>', methods=['PUT'])
def put_planet(planet_id):
    
    planet = Planeta.query.filter_by(id=planet_id).first()

    if not planet:
        return jsonify({
            "msg": "el planeta no existe"
        }), 404

    data = request.json

    planet.name=data.get('name', planet.name)
    planet.rotation_period=data.get('rotation_period', planet.rotation_period)
    planet.diameter=data.get('diameter', planet.diameter)
    planet.gravity=data.get('gravity', planet.gravity)
    planet.orbital_period=data.get('orbital_period', planet.orbital_period)
    planet.population=data.get('population', planet.population)
    planet.climate=data.get('climate', planet.climate)
    planet.surface_water=data.get('surface_water', planet.surface_water)
    planet.terrain=data.get('terrain', planet.terrain)
    
    db.session.commit()

    response_body = {
        "data": planet.serialize()
    }

    return jsonify(response_body), 200

# DELETE: planeta

@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):

    planet = Planeta.query.filter_by(id=planet_id).first()

    if not planet:
        return jsonify({
            "msg": "El planeta no existe"
        }), 404
    db.session.delete(planet)
    db.session.commit()

    return '', 204


# DELETE: Persona
@app.route('/people/<int:people_id>', methods=['DELETE'])
def delete_person(people_id):

    people = Personaje.query.filter_by(id=people_id).first()

    if not people:
        return jsonify({
            "msg": "la persona no existe"
        }), 404

    db.session.delete(people)
    db.session.commit()

    return '', 204


# GET: Todos los favoritos de un usuario
@app.route('/users/favorites', methods=['GET'])
def get_allFavoritos():

    favoritos = Favoritos.query.filter_by(user_id=1)
    response_body = {
        "data": [favorito.serialize() for favorito in favoritos]}

    return jsonify(response_body), 200

# añadior planeta a favoritos


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_planet_to_favorite(planet_id):

    nuevo_favorito = Favoritos(user_id=1, planeta_id=planet_id)
    db.session.add(nuevo_favorito)
    db.session.commit()

    response_body = {
        "data": nuevo_favorito.serialize()
    }

    return jsonify(response_body), 201

# añadir personaje a favoritos


@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_people_to_favorite(people_id):

    nuevo_favorito = Favoritos(user_id=1, personaje_id=people_id)
    db.session.add(nuevo_favorito)
    db.session.commit()

    response_body = {
        "data": nuevo_favorito.serialize()
    }

    return jsonify(response_body), 201

# DELETE: personaje de favoritos


@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def del_people_from_favorite(people_id):

    people = Favoritos.query.filter_by(
        user_id=1, personaje_id=people_id).first()

    if not people:
        return jsonify({
            "msg": "la persona no existe en favoritos"
        }), 404
    db.session.delete(people)
    db.session.commit()

    return '', 204

# DELETE: planeta de favoritos


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def del_planet_from_favorite(planet_id):

    planet = Favoritos.query.filter_by(user_id=1, planeta_id=planet_id).first()

    if not planet:
        return jsonify({
            "msg": "el planeta no existe en favoritos"
        }), 404

    db.session.delete(planet)
    db.session.commit()

    return '', 204


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
