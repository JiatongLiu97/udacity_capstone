import os
import unittest
import json
import time
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie


class appTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['DATABASE_TEST_URL']
        self.casting_assistant = os.environ['CASTING_ASSISTANT']
        self.casting_director = os.environ['CASTING_DIRECTOR']
        self.executive_producer = os.environ['EXECUTIVE_PRODUCER']

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    
    def tearDown(self):
        """Executed after each test"""
        pass

    """
    One test for success behavior of each endpoint
    One test for error behavior of each endpoint
    Two tests of RBAC for each role
    """

    # test GET '/actors' - success case
    def test_get_actors(self):
        # initiate some actors in the database for testing
        actor_1 = Actor(name = 'actor_1', age = 22, gender = 'male')
        actor_1.insert()
        actor_2 = Actor(name = 'actor_2', age = 22, gender = 'male')
        actor_2.insert()
        response = self.client().get('/actors',
            headers={
            "Authorization": "Bearer {}".format(
            self.casting_assistant)
            })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        actors = data['actors']
        self.assertEqual(len(actors), 2)
        self.assertEqual(actors[0]['name'], 'actor_1' or 'actor_2')

    # test GET '/actors' - failure case: can not delete on '/actors'
    def test_get_actors_fail(self):
        response = self.client().delete('/actors',
            headers={
            "Authorization": "Bearer {}".format(
            self.casting_assistant)
            })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['message'], "Invalid method")

    # test GET '/movies' - success case
    def test_get_movies(self):
        # initiate some movies in the database for testing
        movie_1 = Movie(title = 'movie_1', release_date = '2021-1-1')
        movie_1.insert()
        movie_2 = Movie(title = 'movie_2', release_date = '2021-1-1')
        movie_2.insert()

        response = self.client().get('/movies',
            headers={
            "Authorization": "Bearer {}".format(
            self.casting_assistant)
            })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        movies = data['movies']
        self.assertEqual(len(movies), 2)
        self.assertEqual(movies[0]['title'], 'movie_1' or 'movie_2')

    # test GET '/movies' - failure case: can not delete on '/movies'
    def test_get_movies_fail(self):
        response = self.client().delete('/movies',
            headers={
            "Authorization": "Bearer {}".format(self.casting_director)
            }
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['message'], "Invalid method")
    
    # test DELETE '/actors/1' - success case
    def test_delete_actor(self):
        response = self.client().delete('/actors/1',
            headers={
                "Authorization": "Bearer {}".format(self.casting_assistant)
            }
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted id"], 1)
    

    # test DELETE '/actors/1000' - failure case: delete an actor not existing
    def test_delete_actor(self):
        response = self.client().delete('/actors/1000',
            headers={
                "Authorization": "Bearer {}".format(self.casting_director)
            }
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Page not found")

    # test DELETE '/movies/1' - success case
    def test_delete_movie(self):
        response = self.client().delete('/movies/1',
            headers={
                "Authorization": "Bearer {}".format(self.executive_producer)
            }
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted id"], 1)

    # test DELETE '/movies/1000' - failure case: delete a movie not existing
    def test_delete_movie(self):
        response = self.client().delete('/movies/1000',
            headers={
                "Authorization": "Bearer {}".format(self.executive_producer)
            }
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Page not found")

    # test POST '/actors' - success case
    def test_post_actor(self):
        newActor = {
            'name': 'actor_3',
            'age': 23,
            'gender': 'female',
        }
        response = self.client().post('/actors',
            headers={
                "Authorization": "Bearer {}".format(self.casting_assistant)
            },
            json=newActor
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["name"], 'actor_3')

    # test POST '/actors' - failure case: post an actor whos age is a string
    def test_post_actor(self):
        newActor = {
            'name': 'actor_3',
            'age': '23',
            'gender': 'female',
        }
        response = self.client().post('/actors',
            headers={
                "Authorization": "Bearer {}".format(self.casting_assistant)
            },
            json=newActor
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'Unprocessable recource')
    
    # test POST '/movies' - success case
    def test_post_movie(self):
        newMovie = {
            'title': 'movie_3',
            'release_date': '2022-1-1'
        }
        response = self.client().post('/movies',
            headers={
                "Authorization": "Bearer {}".format(self.executive_producer)
            },
            json=newMovie
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["title"], 'movie_3')

    # test POST '/movies' - failure case: post a movie whos release_date is an integer
    def test_post_actor(self):
        newMovie = {
            'title': 'movie_3',
            'release_date': 202211
        }
        response = self.client().post('/movies',
            headers={
                "Authorization": "Bearer {}".format(self.executive_producer)
            },
            json=newMovie
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'Unprocessable recource')

    # test PATCH '/actors/1' - success case
    def test_patch_actor(self):
        editActor = {
            'name': 'new_name',
            'age': None,
            'gender': None
        }
        response = self.client().patch('/actors/1',
            headers={
                "Authorization": "Bearer {}".format(self.casting_director)
            },
            json=editActor
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["name"], 'new_name')

    # test PATCH '/actors/1000' - failure case: patch an actor not existing
    def test_patch_actor(self):
        editActor = {
            'name': 'new_name',
            'age': None,
            'gender': None
        }
        response = self.client().patch('/actors/1000',
            headers={
                "Authorization": "Bearer {}".format(self.casting_director)
            },
            json=editActor
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Page not found")
    
    # test PATCH '/movies/1' - success case
    def test_patch_movie(self):
        editMovie = {
            'title': 'new_title',
            'release_date': None
        }
        response = self.client().patch('/movies/1',
            headers={
                "Authorization": "Bearer {}".format(self.casting_director)
            },
            json=editMovie
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["title"], 'new_title')

    # test PATCH '/movies/1000' - failure case: patch a movie not existing
    def test_patch_movie(self):
        editMovie = {
            'title': 'new_title',
            'release_date': None
        }
        response = self.client().patch('/movies/1000',
            headers={
                "Authorization": "Bearer {}".format(self.casting_director)
            },
            json=editMovie
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Page not found")
    
    # RBAC test for role: Casting assistant
    # test if role: Casting assistant has permission [get '/actors']
    def test_casting_assistant_getActor(self):
        response = self.client().get('/actors',
            headers={
                "Authorization": "Bearer {}".format(self.casting_assistant)
            }
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)

    # RBAC test for role: Casting assistant
    # test that role: Casting assistant does not have permission [delete '/actors/<id>']
    def test_casting_assistant_getActor(self):
        actor_1 = Actor(name = 'actor_1', age = 22, gender = 'male')
        actor_1.insert()
        actor_2 = Actor(name = 'actor_2', age = 22, gender = 'male')
        actor_2.insert()
        response = self.client().delete('/actors/1',
            headers={
                "Authorization": "Bearer {}".format(self.casting_assistant)
            }
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data["code"], "unauthorized")
        self.assertEqual(data["description"], "Permission not found.")

    # RBAC test for role: Casting director
    # test if role-Casting director has permission [post '/actors']
    def test_casting_assistant_getActor(self):
        editActor = {
            'name': 'new_name',
            'age': None,
            'gender': None
        }
        response = self.client().patch('/actors/1',
            headers={
                "Authorization": "Bearer {}".format(self.casting_director)
            },
            json=editActor
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["name"], 'new_name')
    
    # RBAC test for role: Casting director
    # test if role-Casting director does not have permission [post '/movies']
    def test_casting_assistant_getActor(self):
        newMovie = {
            'title': 'movie_3',
            'release_date': '2022-1-1'
        }
        response = self.client().post('/movies',
            headers={
                "Authorization": "Bearer {}".format(self.casting_director)
            },
            json=newMovie
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data["code"], "unauthorized")
        self.assertEqual(data["description"], "Permission not found.")

    # RBAC test for role: Executive producer
    # test if role-Executive producer has permission [post '/movies']
    def test_casting_assistant_getActor(self):
        newMovie = {
            'title': 'movie_3',
            'release_date': '2022-1-1'
        }
        response = self.client().post('/movies',
            headers={
                "Authorization": "Bearer {}".format(self.executive_producer)
            },
            json=newMovie
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["title"], 'movie_3')
    
    # RBAC test for role: Executive producer
    # test if role-Executive producer has permission [delete '/movies']
    def test_casting_assistant_getActor(self):
        newMovie = Movie(title="new_movie", release_date="2022-2-2")
        newMovie.insert()
        newMovie_id = newMovie.id
        response = self.client().delete('/movies/{}'.format(newMovie_id),
            headers={
                "Authorization": "Bearer {}".format(self.executive_producer)
            }
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted id"], str(newMovie_id))


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
