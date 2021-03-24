from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#data usuarios
class User(db.Model):
    __tablename__ = "username_data"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=True)
    bio = db.Column(db.String(200), nullable=False)
    fav_planets = db.relationship("FavList_Planets", backref="user", lazy=True)
    fav_charts = db.relationship("FavList_Charts", backref="user", lazy=True)
    fav_starships = db.relationship("FavList_Starships", backref="user", lazy=True)


    def __repr__(self):
        return f"<username_data {self.username} -  {self.id} - {self.is_active}>"

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "bio": self.bio,
            "fav_planets": list(map(lambda fav_planet: fav_planet.serialize2(), self.fav_planets)),
            "fav_charts": list(map(lambda fav_chart: fav_chart.serialize2(), self.fav_charts)),
            "fav_starships": list(map(lambda fav_starships: fav_starships.serialize2(), self.fav_starships))
            # do not serialize the password, its a security breach
         }


#lista de favoritos
class FavList_Planets(db.Model):
    __tablename__ = 'favlist_planets'
    id = db.Column(db.Integer, primary_key=True)
    id_planets = db.Column(db.Integer,db.ForeignKey("planets_data.id"), nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey("username_data.id"), nullable=False)
    comments = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f"<favlist_planets {self.user_id}>" 
    

    def serialize(self):
        return {
        "id": self.id,
        "id_planet": self.id_planets,
        "name_planet": self.planets_data.name_planet,
        "user_id": self.user_id,
        "user_name": self.user.username,
        "comments": self.comments
        }
    
    def serialize2(self):
        return {
            "id": self.planets_data.id,
            "name_planet": self.planets_data.name_planet,
            "diameter": self.planets_data.diameter,
            "rotation_period": self.planets_data.rotation_period,
            "orbital_period": self.planets_data.orbital_period,
            "gravity": self.planets_data.gravity,
            "population": self.planets_data.population,
            "climate": self.planets_data.climate,
            "terrain": self.planets_data.terrain,
            "surface_water": self.planets_data.surface_water
        }

#Datos de los planetas
class Planets_Data(db.Model):
    __tablename__ = 'planets_data'
    id = db.Column(db.Integer, primary_key=True)
    name_planet = db.Column(db.String(100), nullable=False) 
    diameter = db.Column(db.String(100), nullable=False)
    rotation_period = db.Column(db.Integer, nullable=False)
    orbital_period = db.Column(db.String(100), nullable=False)
    gravity = db.Column(db.String(100), nullable=False)
    gravity_type = db.Column(db.String(100), nullable=False)
    population = db.Column(db.String(100), nullable=False)
    climate = db.Column(db.String(100), nullable=False)
    terrain = db.Column(db.String(100), nullable=False)
    surface_water = db.Column(db.String(15), nullable=False)
    fav_planets_favlist = db.relationship("FavList_Planets", backref="planets_data", lazy=True)

    def __repr__(self):
        return f"<planets_data {self.name_planet} - {self.id}>"

    def serialize(self):
         return {
             "name_planet": self.name_planet,
             "id": self.id
         }

    def serialize_data(self):
        return {
            "id": self.id,
            "name_planet": self.name_planet,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "gravity": self.gravity_type,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water  
        }


 #lista de charts favoritos
class FavList_Charts(db.Model):
     __tablename__ = 'favlist_chart'
     id = db.Column(db.Integer, primary_key=True)
     id_chart = db.Column(db.Integer, db.ForeignKey("chart_data.id"), nullable=False)
     user_id = db.Column(db.Integer, db.ForeignKey("username_data.id"))
     comments = db.Column(db.String(500), nullable=False)

     def __repr__(self):
         return f"<favlist_chart {self.user_id} - {self.id_chart}>"

     def serialize(self):
            return {
                "id": self.id,
                "user_id": self.user_id,
                "name_chart": self.chart_data.name_chart,
                "id_chart": self.id_chart,
                "user_name": self.user.username,
                "comments": self.comments
     }

     def serialize2(self):
         return {
             "id": self.chart_data.id,
             "name_chart": self.chart_data.name_chart,
             "height": self.chart_data.height,
             "mass": self.chart_data.mass,
             "hair_color": self.chart_data.hair_color,
             "skin_color": self.chart_data.skin_color,
             "eye_color": self.chart_data.eye_color,
             "birth_year": self.chart_data.birth_year,
             "gender": self.chart_data.gender
         }


#data de los charts
class Chart_Data(db.Model):
    __tablename__ = 'chart_data'
    id = db.Column(db.Integer, primary_key=True)
    name_chart = db.Column(db.String(100), nullable=False)
    height = db.Column(db.String(100), nullable=False)
    mass = db.Column(db.String(100), nullable=False)
    hair_color = db.Column(db.String(90), nullable=False)
    skin_color = db.Column(db.String(100), nullable=False)
    eye_color = db.Column(db.String(100), nullable=False)
    birth_year  = db.Column(db.String(100), nullable=False)
    gender  = db.Column(db.String(100), nullable=False)
    fav_favlist_chart = db.relationship("FavList_Charts", backref="chart_data")

    def __repr__(self):
        return f"<chart_data {self.name_chart} - {self.id}>"

    def serialize(self):
        return {
            "id": self.id,
            "name_chart": self.name_chart
        }


    def serialize_data(self):
        return {
            "id": self.id,
            "name_chart": self.name_chart,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender
        }


#lista de starships favoritos
class FavList_Starships(db.Model):
     __tablename__ = 'favlist_starships'
     id = db.Column(db.Integer, primary_key=True)
     id_starship = db.Column(db.Integer,db.ForeignKey("starships_data.id"))
     user_id = db.Column(db.Integer,db.ForeignKey("username_data.id"))
     comments = db.Column(db.String(500), nullable=False)

     def __repr__(self):
         return f"<favlist_starships {self.user_id} - {self.id_starship}>"

     def serialize(self):
            return {
                "id": self.id,
                "user_id": self.user_id,
                "name_starship": self.starships_data.name_starship,
                "id_starship": self.id_starship,
                "user_name": self.user.username,
                "comments": self.comments
     }

     def serialize2(self):
         return {
             "id": self.starships_data.id,
             "name_starship": self.starships_data.name_starship,
             "model": self.starships_data.model,
             "startship_class": self.starships_data.starship_class,
             "manufacturer": self.starships_data.manufacturer,
             "cost_in_credits": self.starships_data.cost_in_credits,
             "length": self.starships_data.length,
             "crew": self.starships_data.crew,
             "passengers": self.starships_data.passengers,
             "max_atmosphering_speed": self.starships_data.max_atmosphering_speed,
             "hyperdrive_rating": self.starships_data.hyperdrive_rating,
             "MGLT": self.starships_data.MGLT,
             "cargo_capacity": self.starships_data.cargo_capacity,
             "consumables": self.starships_data.consumables,
             "pilots": self.starships_data.pilots
         }

#starships data
class Starships_Data(db.Model):
    __tablename__ = 'starships_data'
    id = db.Column(db.Integer, primary_key=True)
    name_starship = db.Column(db.String(100),nullable=False)
    model = db.Column(db.String(250),unique=True, nullable=False)
    starship_class = db.Column(db.String(250), nullable=False) 
    manufacturer = db.Column(db.String(120), nullable=False)
    cost_in_credits = db.Column(db.String(100) , nullable=False)
    length = db.Column(db.String(100), nullable=False)
    crew = db.Column(db.String(100), nullable=False)
    passengers = db.Column(db.String(100), nullable=False)
    max_atmosphering_speed = db.Column(db.String(100), nullable=False)
    hyperdrive_rating = db.Column(db.String(100), nullable=False) 
    MGLT = db.Column(db.String(100), nullable=False) 
    cargo_capacity = db.Column(db.String(100), nullable=False) 
    consumables = db.Column(db.String(25), nullable=False) 
    pilots = db.Column(db.String(20), nullable=False)
    fav_favlist_starships = db.relationship("FavList_Starships", backref="starships_data")

    def __repr__(self):
        return f"<starships_data {self.name_starship}>"

    def serialize(self):
        return {
            "id": self.id,
            "name_starship": self.name_starship,
        }

    def serialize_data(self):
       return {
           "id": self.id,
           "name_starship": self.name_starship,
           "model": self.model,
           "starship_class": self.starship_class,
           "manufacturer": self.manufacturer,
           "cost_in_credits": self.cost_in_credits,
           "length": self.length,
           "crew": self.crew,
           "passengers":self.passengers,
           "max_atmosphering_speed": self.max_atmosphering_speed,
           "hyperdrive_rating": self.hyperdrive_rating,
           "MGLT": self.MGLT,
           "cargo_capacity": self.cargo_capacity,
           "consumables": self.consumables,
           "pilots": self.pilots
        }


#- $ pipenv run migrate create database migrations (if models.py is edited)
#- $ pipenv run upgrade run database migrations (if pending)
#- $ pipenv run start start flask web server (if not running)
#- $ pipenv run deploy deploy to heroku (if needed) 