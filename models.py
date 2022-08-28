import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

'''
Movies with attributes title and release date
'''
class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(db.Integer, primary_key=True)
    title = Column(db.String)
    release_date = Column(db.String)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    '''
    format()
        return the movie model in json form
    '''
    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date}

    '''
    insert()
        inserts a new movie model into database
        the new movie has a title and a release date
        EXAMPLE
            movie = Movie(title=new_title, release_date=new_release_date)
            movie.insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes an existing moive model in database
        the model must exist in the database
        EXAMPLE
            movie = Movie(title=new_title, release_date=new_release_date)
            movie.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates an existing moive model in database
        the model must exist in the database
        EXAMPLE
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            movie.title = 'Superman'
            movie.update()
    '''
    def update(self):
        db.session.commit()

'''
Actors with attributes name, age and gender
'''
class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String)
    age = Column(db.Integer)
    gender = Column(db.String)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    '''
    format()
        return the actor model in json form
    '''
    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,}

    '''
    insert()
        inserts a new actor model into database
        the new actor has a name, age and gender attributes
        EXAMPLE
            actor = Actor(name=new_name, age=new_age, gender=new_gender)
            actor.insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes an existing actor model in database
        the model must exist in the database
        EXAMPLE
            actor = Actor(name=new_name, age=new_age, gender=new_gender)
            actor.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates an existing actor model in database
        the model must exist in the database
        EXAMPLE
            actor = Actor.query.filter(Actor.id == id).one_or_none()
            actor.name = 'Tony'
            actor.update()
    '''
    def update(self):
        db.session.commit()

    
