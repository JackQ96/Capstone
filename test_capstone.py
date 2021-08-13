import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movies, Actors


DB_USER = os.getenv('DB_USER', 'demo1')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'pass1')
DB_NAME = os.getenv('DB_NAME', 'capstone')
DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5000')





class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = DB_NAME
        self.database_path = "postgresql+psycopg2://{}:{}@{}/{}".format(DB_USER,DB_PASSWORD,
        DB_HOST, self.database_name)
        self.PRODUCER_JWT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InhJVEtoa2NnSjNBNHU0SjBoMjBxVCJ9.eyJpc3MiOiJodHRwczovL2phY2txLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTEyYzdlY2MxZmRjYjAwNzE5Yjk5NWYiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTYyODc5MjA2NCwiZXhwIjoxNjI4Nzk5MjY0LCJhenAiOiJOQjhOcDlkU2dOS29MUUU5ZDlzc21uajlhdDZGOEVmRyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyJdfQ.h7V-Cg4-BCvIsA64Zxj07OAT0oA40l7riLWexEHF_PW8oLm_02IgP0moiDbTseISbSWl4YMaaI53ujRDanC38PzM1umJMTiFxLvDcwyiPLZLO8_JUdsh5woHF_eAVEu1kkzh2IOJA6Y6_4bszs-efI5XJnjDQXdFAoIRtwKLywE9VA2n8VjiEAptYVtwuyoAxBXfldBjj8KPbqO65SDAhBYxATF4qlMwd-yzwJK-Qs77SrQ2XC-RHpvSg84AOtPTocAz4sJDaWZC9Mri2T-475QAVzKGGfb2hX9QO4sEJ6kSaEdtP9TgiJu2CR_nD1Hoa92TZtVp91EfrzvpBFwwGw'
        self.CASTING_AGENT_JWT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InhJVEtoa2NnSjNBNHU0SjBoMjBxVCJ9.eyJpc3MiOiJodHRwczovL2phY2txLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTEyYzg0YTFjNWFlZjAwNmFlNDA5NmMiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTYyODc5MjIxOSwiZXhwIjoxNjI4Nzk5NDE5LCJhenAiOiJOQjhOcDlkU2dOS29MUUU5ZDlzc21uajlhdDZGOEVmRyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.GLyBXUMkvBVO1YPy69FM1485XWIsNUTQUYn2DhvswEv9e8wbc9jYDStzrCSimIzHWMhKH-Zdb0Eb2CoZixFXhEh6r7ByC3sQTmmvSeBLCv1z2J70cWWH341Mdu1znHOHf7_x7T7Zob5eisGz_kmN12FJt-BhHLbfJZOcGUXh5YoVA89-al4N1XEZnG2V1I7ZKsab2uWQVR94UNfVA9ivKwxrgSiPI78W_0NlYLiPG77cjR84mMGirjGKBD_Ll2psSo1Ha1ohsRfZNE9y2d1or7tsLI3hIfYdv-pv7vkSEuBJLYnf_WK0pQ0ANSjb_PQDijkK7HeZlryQLC4-AvPXxg'
        setup_db(self.app, self.database_path)


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


    def test_get_movies_agent(self):
        res = self.client().get('/movies',
            headers={'Authorization': 'Bearer' + self.CASTING_AGENT_JWT
            })

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_get_movies_unauthorized(self):
        res = self.client().get('/movies')

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unauthorized')

    # ---- GET Actors Tests ----

    def test_get_movies_agent(self):
        res = self.client().get('/actors',
            headers={'Authorization': 'Bearer' + self.CASTING_AGENT_JWT
            })

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_get_movies_unauthorized(self):
        res = self.client().get('/actors')

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unauthorized')


    # ---- Post Movie Tests ----

    def test_post_movie(self):
        res = self.client().post('/movies', json=self.movie, headers= {
            'Authorization': 'Bearer' + self.PRODUCER_JWT
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['new_movie'])

    def test_post_movie_unauthorized(self):
        res = self.client().post('/movies', json=self.movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Unauthorized')
    

    # ---- Post Actor Tests ----

    def test_post_actor(self):
        res = self.client().post('/actors', json=self.actor, headers= {
            'Authorization': 'Bearer' + self.PRODUCER_JWT
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['new_actor'])

    def test_post_actor_unauthorized(self):
        res = self.client().post('/actors', json=self.actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Unauthorized')
    
    # ---- Patch Movie Tests ----

    def test_patch_movie(self):
        res = self.client().patch('/movies/1', json={'title': 'changed'}, headers={
            'Authorization': 'Bearer' + self.PRODUCER_JWT
        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['changed_movie'])

        def test_patch_movie(self):
            res = self.client().patch('/movies/1', json={'title': 'changed'})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 401)
            self.assertEqual(data['success'], False)
            self.assertTrue(data['message'], 'Unauthorized')

    # ---- Patch Actor Tests ----

    def test_patch_actor(self):
        res = self.client().patch('/actors/1', json={'name': 'changed'}, headers={
            'Authorization': 'Bearer' + self.PRODUCER_JWT
        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['changed_actor'])

    def test_patch_actor_unauthorized(self):
        res = self.client().patch('/actors/1', json={'name': 'changed'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Unauthorized')

    # ---- Delete Movie Tests ----

    def test_delete_movie(self):
        res = self.client().delete('/movies/1', headers={
            'Authorization': 'Bearer' + self.PRODUCER_JWT
        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted_movie'])

    def test_delete_movie_unauthorized(self):
        res = self.client().delete('/movies/1')

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Unauthorized')

    
    # ---- Delete Actor Tests ----

    def test_delete_actor(self):
        res = self.client().delete('/actors/1', headers={
            'Authorization': 'Bearer' + self.PRODUCER_JWT
        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted_actor'])

    def test_delete_actor_unauthorized(self):
        res = self.client().delete('/actors/1')

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Unauthorized')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()