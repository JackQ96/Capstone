import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movies, Actors
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv('DB_USER', 'demo1')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'pass1')
DB_NAME = os.getenv('DB_NAME', 'capstone')
DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5000')


PRODUCER = os.environ.get('PRODUCER_JWT')
CASTING_AGENT = os.environ.get('CASTING_JWT')


def get_headers(payload):
    return {'Authorization': f'Bearer {payload}'}


class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = DB_NAME
        self.database_path = "postgresql+psycopg2://{}:{}@{}/{}".format(DB_USER, DB_PASSWORD,
        DB_HOST, self.database_name)
        setup_db(self.app)
        self.actor = {
            'name': 'Jack',
            'gender': 'male',
            'age': '25',
        }
        self.movie = {
            'title': 'Udacity',
            'release_year': '2021',
            'genre': 'action'
        }
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

   
   # ---- GET Movies Tests ----


    # def test_get_movies_agent(self):
    #     res = self.client().get('/movies', 
    #     headers=get_headers(CASTING_AGENT))

    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['movies'])

    # def test_get_movies_unauthorized(self):
    #     res = self.client().get('/movies')

    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 401)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'Authorization header is expected.')

    # # # # ---- GET Actors Tests ----

    # def test_get_actors_agent(self):
    #     res = self.client().get('/actors',
    #         headers=get_headers(CASTING_AGENT))

    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['actors'])

    # def test_get_actors_unauthorized(self):
    #     res = self.client().get('/actors')

    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 401)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'Authorization header is expected.')


    # # ---- Post Movie Tests ----

    # def test_post_movie(self):
    #     res = self.client().post('/movies', json=self.movie, headers=get_headers(PRODUCER))
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['movie'])

    # def test_post_movie_unauthorized(self):
    #     res = self.client().post('/movies', json=self.movie)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 401)
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['message'], 'Authorization header is expected.')
    

    # # ---- Post Actor Tests ----

    # def test_post_actor(self):
    #     res = self.client().post('/actors', json=self.actor, headers=get_headers(PRODUCER))
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['actor'])

    # def test_post_actor_unauthorized(self):
    #     res = self.client().post('/actors', json=self.actor)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 401)
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['message'], 'Authorization header is expected.')
    
    # # ---- Patch Movie Tests ----

    def test_patch_movie(self):
        res = self.client().patch('/movies/5', json={"title": "testing"}, headers=get_headers(PRODUCER))

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['changed_movie'])

    #     def test_patch_movie_unauthorized(self):
    #         res = self.client().patch('/movies/1', json={'title': 'changed'})
    #         data = json.loads(res.data)

    #         self.assertEqual(res.status_code, 401)
    #         self.assertEqual(data['success'], False)
    #         self.assertTrue(data['message'], 'Authorization header is expected.')

    # # ---- Patch Actor Tests ----

    # def test_patch_actor(self):
    #     res = self.client().patch('/actors/4', json={'name': 'changed'}, headers=get_headers(PRODUCER))

    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['changed_actor'])

    # def test_patch_actor_unauthorized(self):
    #     res = self.client().patch('/actors/1', json={'name': 'changed'})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 401)
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['message'], 'Authorization header is expected.')

    # # ---- Delete Movie Tests ----

    # def test_delete_movie(self):
    #     res = self.client().delete('/movies/3', headers=get_headers(PRODUCER))

    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['deleted_movie'])

    # def test_delete_movie_unauthorized(self):
    #     res = self.client().delete('/movies/3')

    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 401)
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['message'], 'Authorization header is expected.')

    
    # # ---- Delete Actor Tests ----

    # def test_delete_actor(self):
    #     res = self.client().delete('/actors/3', headers=get_headers(PRODUCER))

    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['deleted_actor'])

    # def test_delete_actor_unauthorized(self):
    #     res = self.client().delete('/actors/3')

    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 401)
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['message'], 'Authorization header is expected.')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()