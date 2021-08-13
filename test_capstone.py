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
        self.database_path = "postgresql+psycopg2://{}:{}@{}/{}".format(DB_USER, DB_PASSWORD,
        DB_HOST, self.database_name)
        self.PRODUCER_JWT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InhJVEtoa2NnSjNBNHU0SjBoMjBxVCJ9.eyJpc3MiOiJodHRwczovL2phY2txLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTEyYzdlY2MxZmRjYjAwNzE5Yjk5NWYiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTYyODg4ODI0MiwiZXhwIjoxNjI4ODk1NDQyLCJhenAiOiJOQjhOcDlkU2dOS29MUUU5ZDlzc21uajlhdDZGOEVmRyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyJdfQ.Bm3TmnVaT17cWGEmbOMpvdiz34ROBkZsJ6biUOQStsGFqojXW3BMVW4SI5iLpeklTW4poYnSGuVbp5YTOASj7jqq1SqSHShM3_cl-MhCHuJLKolQmtw_rQF3Yh7SaLcWHW9sMZx-x-pfv8jXI6SEp-DzCdFGYA1_VlUDEPJIHAzAwvcGMEbv6Ng3Gc5RMrUtZer9V0v5XegW6k3RZXbKd8om4CIcz2Li8K1GhSRAzu0kZNK9CVDKh6JiMo0cunFuN2hHtthkbhbgxVuGl7adLXUzR0jeH4dWN7pNLVxMtifVjPWFhvsU2HjOa2SUwpZl41Fd3_pTlBh5WDriCblY2Q'
        self.CASTING_AGENT_JWT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InhJVEtoa2NnSjNBNHU0SjBoMjBxVCJ9.eyJpc3MiOiJodHRwczovL2phY2txLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTEyYzg0YTFjNWFlZjAwNmFlNDA5NmMiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTYyODg4ODQ0NCwiZXhwIjoxNjI4ODk1NjQ0LCJhenAiOiJOQjhOcDlkU2dOS29MUUU5ZDlzc21uajlhdDZGOEVmRyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.Ico7aoYPubcQrgl787tDHwd83l7Jv7T10arMB7esv27VlkM5wF7IjDa0UVtPIuxf0Gpy8ajFs-pVFWsLmoMKu1m0EowQou1HAZPkO6zkNsLV8aT8KZMgLSa-sxL-fGtDB2KLrmK9U8QxLsThO_j2OkbWAWJyGMAmhdD25TqINpNjZv-iBxolqyUU5pWbt58U1rSbhhf8jgzAblEV-Ixc9nzxute1UKo6KLNwZsmhV8khgnYtTsiT3jG412f2eISgYoVpQyWNdcKr-7U2kClvHcl4hCkLAfOKAqw_2K9Vz3QkS_-sXrlA_X8UUW5o_joRkDLuNEJn2Jap6uDIAlAhqQ'
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