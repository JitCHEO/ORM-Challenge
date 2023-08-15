from flask import Flask, request #, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields, validate 
app = Flask(__name__)
ma = Marshmallow(app)

## DB CONNECTION AREA
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://jitkcheo:@localhost:5432/ripe_tomatoes_db"

#create the database instance
db = SQLAlchemy(app)


# CLI COMMANDS AREA
@app.cli.command("create")
def create_tables():
    db.create_all()
    print("tables created")

@app.cli.command("seed")
def seed_tables():
    movie1 = Movie(
        title = 'Brisbane Traffic Solver',
        description = 'description goes here...'
    )
    db.session.add(movie1)

    movie2 = Movie(
        title = 'Sustainability coding board game',
        description = 'description goes here...'
    )
    db.session.add(movie2)

    actor1 = Actor(
        first_name = 'John',
        last_name = ' Holland',
        gender = 'Male',
        country = 'Austrlia',
        date_of_birth = '02-02-1990'
    )
    db.session.add(actor1)

    actor2 = Actor(
        first_name = 'Mary',
        last_name = ' Liz',
        gender = 'Female',
        country = 'Austrlia',
        date_of_birth = '03-02-1980'
    )
    db.session.add(actor2)
    db.session.commit()
    print("tables seeded")

@app.cli.command('drop')
def drop_tables():
    db.drop_all()
    print("tables dropped")

# MODELS AREA

class Movie(db.Model):
    __tablename__ = "movies"
    
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String())
    description = db.Column(db.String())

class Actor(db.Model):
    __tablename__ = "actors"
    
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    gender = db.Column(db.String())
    country = db.Column(db.String())
    date_of_birth = db.Column(db.String())
  

# SCHEMAS AREA

class MovieSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "description")
    title = fields.String(required=True, validate=validate.Length(min=5, max=50))

movies_schema = MovieSchema(many=True)
movie_schema = MovieSchema()

class ActorSchema(ma.Schema):
    class Meta:
        fields = ("id", "first_name", "last_name", "gender", "country", "date_of_birth")
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)

actors_schema = ActorSchema(many=True)
actor_schema = ActorSchema()

# ROUTING AREA

@app.route("/")
def hello():
  return "Welcome to Ripe Tomatoes API"

@app.get('/movies')
def get_movies():
    #prepare the query to get data SELECT * FROM PROJECTS
    stmt = db.select(Movie)
    #get the data
    movie = db.session.scalars(stmt)
    #convert the db data into something readable by Python
    result = movies_schema.dump(movie)

    return result
    #return jsonify(result)

@app.get('/actors')
def get_actors():
    #prepare the query to get data SELECT * FROM PROJECTS
    stmt = db.select(Actor)
    #get the data
    actor = db.session.scalars(stmt)
    #convert the db data into something readable by Python
    result = actors_schema.dump(actor)

    return result
    #return jsonify(result)


if __name__ == "__main__":
    app.run()

