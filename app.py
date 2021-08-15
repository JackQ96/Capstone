import os
import json
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import app, setup_db, db_drop_and_create_all, Movies, Actors
from flask_cors import CORS
from auth import AuthError, requires_auth


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    # db_drop_and_create_all()

# -------Actors-------
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        try:
            actors = Actors.query.all()
            if len(actors) == 0:
                abort(404)
            else:
                format_actors = [actors.format() for actor in actors]
                return jsonify({
                    'success': True,
                    'actors': format_actors
                }), 200
        except Exception as error:
            abort(422)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def post_actors(payload):
        data = request.get_json()

        new_name = data.get('name', None)
        new_gender = data.get('gender', None)
        new_age = data.get('age', None)

        try:
            new_actor = Actors(name=new_name, gender=new_gender, age=new_age)

            new_actor.insert()

            return jsonify({
                'success': True,
                'actor': new_actor.format()
            }), 200

        except Exception as error:
            abort(422)

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def patch_actors(payload, id):
        data = request.get_json()

        edit_name = data.get('name', None)
        edit_gender = data.get('gender', None)
        edit_age = data.get('age', None)

        try:
            edit_actor = Actors.query.filter(Actors.id == id)
            edit_actor.name = edit_name
            edit_actor.gender = edit_gender
            edit_actor.age = edit_age

            if len(edit_actor) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'actor': edit_actor.format()
            }), 200
        except Exception as error:
            abort(422)

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors(payload, id):
        try:
            actor = Actors.query.filter_by(id=id).first()
            if len(actor) == 0:
                abort(404)
            else:
                actor.delete()
            return jsonify({
                'success': True,
                'message': 'Actor deleted'
            }), 200
        except Exception as error:
            abort(422)

    # -------Movies-------
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        try:
            movies = Movies.query.all()
            if len(movies) == 0:
                abort(404)
            else:
                format_movies = [movies.format() for movie in movies]
            return jsonify({
                'success': True,
                'movies': format_movies
            }), 200
        except Exception:
            abort(422)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def post_movies(payload):
        data = request.get_json()
        new_title = data.get('title', None)
        new_release_year = data.get('release_year', None)
        new_genre = data.get('genre', None)

        try:
            new_movie = Movies(title=new_title,
                               release_year=new_release_year, genre=new_genre)
            new_movie.insert()
            return jsonify({
              'success': True,
              'movie': new_movie.format()
            }), 200
        except Exception as error:
            abort(422)

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def patch_movies(payload, id):
        data = request.get_json()
        edit_title = data.get('title', None)
        edit_release_year = data.get('release_year', None)
        edit_genre = data.get('genre', None)

        try:
            edit_movie = Movies.query.filter(Movies.id == id)
            edit_movie.title = edit_title
            edit_movie.release_year = edit_release_year
            edit_movie.genre = edit_genre

            if len(edit_movie) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'movie': edit_movie.format()
            }), 200
        except Exception as error:
            abort(422)

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies(payload, id):
        try:
            movie = Movies.query.filter_by(id=id).first()
            if len(movie) == 0:
                abort(404)
            else:
                movie.delete()
            return jsonify({
                'success': True,
                'message': 'Movie deleted'
            }), 200

        except Exception as error:
            abort(422)

    # -------Error Handlers-------
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'message': 'Not Found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'message': 'Unable to process'
        }), 422

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            'success': False,
            'message': 'Auth Error'
        }), AuthError

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'message': 'Unauthorized attempt'
        }), 401

    return app


app = create_app()
if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
