"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, json
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, JWTManager
from admin import setup_admin
from models import db, User, Planets_Data, Chart_Data, Starships_Data, FavList_Planets, FavList_Charts,  FavList_Starships
import datetime
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)



#users FUNCTIONS

#get all users
@app.route('/users', methods=['GET'])
def get_all_users():
    all_users = User.query.all()
    all_users_serialized = list(map(lambda user: user.serialize(), all_users))
    return jsonify(all_users_serialized),200

#get only user
@app.route('/user/<int:id>', methods=['GET'])
def get_only_user(id):
    only_user = User.query.filter_by(id=id).first()
    if not only_user:
        return jsonify({"msg": "user not found"}),404
    only_user = only_user.serialize()
    return jsonify(only_user),200

#######################################
#Register

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.json.get("username", None)
        email = request.json.get("email", None)
        password = request.json.get("password", None)
        bio = request.json.get("bio", None)

    if not username:
        return jsonify({"msg": "The username is required" }), 404
    if not email:
        return jsonify({"msg": "The email is required"}), 404
    if not password:
        return jsonify({'msg': "The password is required"}), 404
    if not bio:
        return jsonify({'msg': "The bio is required"}), 404
    
    new_user = User(username=username, email=email, password=generate_password_hash(password), bio=bio)

    db.session.add(new_user)
    db.session.commit()

    return jsonify("All good, new user add")



#################################
#Login
@app.route('/starSession', methods=['POST'])
def starSession():
    if request.method == 'POST':
        email = request.json.get("email", None)
        password = request.json.get("password", None)

    if not email:
        return jsonify({'msg': "The email is required for login"}), 404
    if not password:
        return jsonify({'msg': "The password is required for login"}), 404

    Find_user = User.query.filter_by(email=email).first()

    if not Find_user:
        return jsonify({'msg': "The email or password is incorrect"}),404
    if not check_password_hash(Find_user.password, password):
        return jsonify({'msg': "The email or password is incorrect"}),404

    expires=datetime.timedelta(days=2)
    access_token = create_access_token(indentity=Find_user.email, expires_delta=expires)

    data = {
        "token": access_token,
        "successful": True
    }

    return jsonify(data), 200


    


    
#FUNCTIONS de los favoritos

#list de favoritos de todos planetas
@app.route('/favorites/planets', methods=['GET'])
def get_all_favorites_planets():
    all_favorites_planets =  FavList_Planets.query.all()
    all_favorites_planets = list(map(lambda all_favorites: all_favorites.serialize(), all_favorites_planets)),
    return jsonify(all_favorites_planets), 200

#list de cada planeta favorito
@app.route('/favorite/planet/<int:id>', methods=['GET'])
def get_only_favorite(id):
    only_favorite_planet = FavList_Planets.query.filter_by(id=id).first()
    if not only_favorite_planet:
        return jsonify({"msg": "favorite not found"}),404
    only_favorite_planet = only_favorite_planet.serialize()
    return jsonify(only_favorite_planet)


#list de todos los charts favoritos
@app.route('/favorites/charts', methods=['GET'])
def get_all_favorites_charts():
    all_favorites_charts = FavList_Charts.query.all()
    all_favorites_charts = list(map(lambda all_charts: all_charts.serialize(), all_favorites_charts))
    return jsonify(all_favorites_charts)


#list de cada chart favorito
@app.route('/favorite/chart/<int:id>', methods=['GET'])
def get_only_favorite_chart(id):
    only_favorite_chart = FavList_Charts.query.filter_by(id=id).first()
    if not only_favorite_chart:
        return jsonify({"msg": "favorite chart not found"}),404
    only_favorite_chart = only_favorite_chart.serialize()
    return jsonify(only_favorite_chart)


#list de todos los starships favoritos
@app.route('/favorites/starships', methods=['GET'])
def get_all_favorites_starships():
    all_favorites_starships = FavList_Starships.query.all()
    all_favorites_starships = list(map(lambda favorites_starships: favorites_starships.serialize(), all_favorites_starships))
    return jsonify(all_favorites_starships)


#list de cada starship favorito
@app.route('/favorite/starship/<int:id>', methods=['GET'])
def get_only_favorite_starship(id):
    only_favorite_starship = FavList_Starships.query.filter_by(id=id).first()
    if not only_favorite_starship:
        return jsonify({"msg": "starship favorite not found"}),404
    only_favorite_starship = only_favorite_starship.serialize()
    return jsonify(only_favorite_starship)

    
#FUNCTIONS PLANETS

#get all information planets
@app.route('/planets', methods=['GET'])
def show_all_planets():
    all_planets = Planets_Data.query.all()
    all_planets_serialized = list(map(lambda planets: planets.serialize(), all_planets))
    return jsonify(all_planets_serialized),200


    
#get only planet
@app.route('/planet/<int:id>', methods=['GET']) 
def get_only_planet(id):
    only_planet = Planets_Data.query.filter_by(id=id).first()
    if not only_planet:
        return jsonify({"msg":"Planet not found"}),404
    only_planet = only_planet.serialize()
    return jsonify(only_planet),200



#get all data planet
@app.route('/planet/data', methods=['GET'])
def get_planet_data():
    planet_data = Planets_Data.query.all()
    planet_data_serialized = list(map(lambda data: data.serialize_data(), planet_data))
    return jsonify(planet_data_serialized),200





#FUNCTIONS CHARTS

#get all info charts
@app.route('/charts', methods=['GET'])
def show_all_charts():
    all_charts = Chart_Data.query.all()
    all_charts_serialized = list(map(lambda charts: charts.serialize(), all_charts))
    return jsonify(all_charts_serialized), 200



 #get only chart
@app.route('/chart/<int:id>', methods=['GET'])
def get_only_chart(id):
    only_chart = Chart_Data.query.filter_by(id=id).first()
    if not only_chart:
        return jsonify({"msg": "chart not found"}),404
    only_chart = only_chart.serialize()
    return jsonify(only_chart),200



#get all data chart
@app.route('/chart/data', methods=['GET'])
def get_chart_data():
    chart_data = Chart_Data.query.all()
    char_data_serialized = list(map(lambda data: data.serialize_data(), chart_data))
    return jsonify(char_data_serialized),200




#FUNCTIONS STARSHIPS 

#get all info starships   
@app.route('/starships', methods=['GET'])
def show_all_starships():
    all_starships = Starships_Data.query.all()
    all_starships_serialized = list(map(lambda starships: starships.serialize(), all_starships))
    return jsonify(all_starships_serialized),200



#get only starship
@app.route('/starship/<int:id>', methods=['GET'])
def get_only_starship(id):
    only_starship = Starships_Data.query.filter_by(id=id).first()
    if not only_starship:
        return jsonify({"msg": "starship not found"}),404
    only_starship = only_starship.serialize()
    return jsonify(only_starship),200



#get all data starship
@app.route('/starship/data', methods=['GET'])
def get_starship_data():
    starship_data = Starships_Data.query.all()
    starship_data_serialized = list(map(lambda data: data.serialize_data(), starship_data))
    return jsonify(starship_data_serialized),200




# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

