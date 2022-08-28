from ast import Str
import os
from unittest.util import strclass
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from auth import AuthError, requires_auth
from models import setup_db, Actor, Movie

def create_app(test_config=None):
  
    # initiate app and database
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def get_greeting():
      greeting = "Hello, you are in capstone!" 
      return greeting

    @app.route('/redirect')
    def after_login():
      greeting = "you have logged in!" 
      return greeting

    '''
    Endpoint to get all actors in database
        roles with permission: Casting Assistant, Casting Director, Executive Producer
    '''
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        try:
            return jsonify({
                'success': True,
                'actors': [actor.format() for actor in Actor.query.all()]
            }), 200
        except:
            abort(422)

    '''
    Endpoint to get all actors in database
        roles with permission: Casting Assistant, Casting Director, Executive Producer
    '''
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        try:
            return jsonify({
                'success': True,
                'movies': [movie.format() for movie in Movie.query.all()]
            }), 200
        except:
            abort(422)

    '''
    Endpoint to delete an actor with a specified id in database
        roles with permission: Casting Director, Executive Producer
    '''
    @app.route('/actors/<id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, id):
        actor = Actor.query.filter_by(id=id).one_or_none()
        # if the drink is not found, rise 404 erro
        if actor is None:
            abort(404)
        
        try:
            # delete the actor from database
            actor.delete()
            return jsonify({
                'success': True,
                'deleted id': id
            }), 200
        except:
            abort(422)

    '''
    Endpoint to delete a movie with a specified id in database
        roles with permission: Executive Producer
    '''
    @app.route('/movies/<id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, id):
        movie = Movie.query.filter_by(id=id).one_or_none()
        # if the movie is not found, rise 404 erro
        if movie is None:
            abort(404)
        
        try:
            # delete the movie from database
            movie.delete()
            return jsonify({
                'success': True,
                'deleted id': id
            }), 200
        except:
            abort(422)

    '''
    Endpoint to post an actor into database
        roles with permission: Casting Director, Executive Producer
    '''
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actor(payload):
        # get the body from request
        body = request.get_json()

        # get parameters of the actor to be added
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)

        try:
            actor = Actor(name = name, age = age, gender = gender)
            actor.insert()
            return jsonify({
                'success': True,
                'name': actor.name
            }), 200
        except:
            abort(422)

    '''
    Endpoint to post a movie into database
        roles with permission: Executive Producer
    '''
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(payload):
        # get the body from request
        body = request.get_json()

        # get parameters of the movie to be added
        title = body.get('title', None)
        release_date = body.get('release_date', None)
        if not isinstance(release_date, str):
          abort(422)

        try:
            movie = Movie(title = title, release_date = release_date)
            movie.insert()
            return jsonify({
                'success': True,
                'title': movie.title
            }), 200
        except:
            abort(422)

    '''
    Endpoint to modify an existing actor with specified id in database
        roles with permission: Casting Director, Executive Producer
    '''
    @app.route('/actors/<id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def edit_actor(payload, id):
        actor = Actor.query.filter_by(id=id).one_or_none()
        # if the actor is not found, rise 404 erro
        if actor is None:
            abort(404)
        
        # get the body from request
        body = request.get_json()

        # get parameters of the actor to be edited
        newName = body.get('name', None)
        newAge = body.get('age', None)
        newGender = body.get('gender', None)
        
        try:
            if newName is not None:
                actor.name = newName
            if newAge is not None:
                actor.age = newAge
            if newGender is not None:
                actor.gender = newGender
            actor.update()
            return jsonify({
                'success': True,
                'name': actor.name
            }), 200
        except:
            abort(422)

    '''
    Endpoint to modify an existing movie with specified id in database
        roles with permission: Casting Director, Executive Producer
    '''
    @app.route('/movies/<id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def edit_movie(payload, id):
        movie = Movie.query.filter_by(id=id).one_or_none()
        # if the movie is not found, rise 404 erro
        if movie is None:
            abort(404)
        
        # get the body from request
        body = request.get_json()

        # get parameters of the movie to be edited
        newTitle = body.get('title', None)
        newReleaseDate = body.get('release_date', None)
        try:
            if newTitle is not None:
                movie.title = newTitle
            if newReleaseDate is not None:
                movie.release_date = newReleaseDate
            movie.update()
            return jsonify({
                'success': True,
                'title': movie.title
            }), 200
        except:
            print("why???????????????")
            abort(422)
        

    #error handlers
    @app.errorhandler(400)
    def bad_request(error):
      return jsonify({
          "success": False,
          'error': 400,
          "message": "Bad request"
      }), 400

    @app.errorhandler(404)
    def page_not_found(error):
      return jsonify({
          "success": False,
          'error': 404,
          "message": "Page not found"
      }), 404

    @app.errorhandler(422)
    def unprocessable_recource(error):
      return jsonify({
          "success": False,
          'error': 422,
          "message": "Unprocessable recource"
      }), 422
    
    @app.errorhandler(405)
    def invalid_method(error):
      return jsonify({
          "success": False,
          'error': 405,
          "message": "Invalid method"
      }), 405

    @app.errorhandler(AuthError)
    def handle_auth_error(error):
        response = jsonify(error.error)
        response.status_code = error.status_code
        return response
    
    
    return app

    

app = create_app()

if __name__ == '__main__':
    app.run()
