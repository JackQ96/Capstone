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
                format_actors = [actor.format() for actor in actors]
                return jsonify({
                    'success': True,
                    'actors': format_actors
                }), 200
        except Exception as error:
            print(sys.exc_info)
            abort(422)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def post_actors(pyload):
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
    def patch_actors(pyload, id):
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
    def delete_actors(pyload, id):
        try:
            actor = Actors.query.filter_by(id=id).first()
            format_actor = actor.format()

            if len(format_actor) == 0:
                abort(404)

            actor.delete()
            return jsonify({
                'success': True,
                'deleted_actor': format_actor
            }), 200
        except Exception as error:
            abort(422)

    # -------Movies-------
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(pyload):
        try:
            movies = Movies.query.order_by(Movies.id).all()
            if len(movies) == 0:
                abort(404)
            else:
                format_movies = [movie.format() for movie in movies]
                return jsonify({
                    'success': True,
                    'movies': format_movies
                }), 200
        except Exception:
            print(exc_info)
            abort(422)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def post_movies(pyload):
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
    def patch_movies(pyload, id):
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
            else:
                print(exc_info)
                return jsonify({
                    'success': True,
                    'movie': edit_movie.format()
                }), 200
        except Exception as error:
            abort(422)

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies(pyload, id):
        try:
            movie = Movies.query.filter_by(id=id).first()
            format_movie = movie.format()

            if len(format_movie) == 0:
                abort(404)

            movie.delete()
            return jsonify({
                'success': True,
                'deleted_movie': format_movie
            }), 200

        except Exception as error:
            print(sys.exc_info)
            abort(422)

    # -------Error Handlers-------
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "message": 'Not Found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "message": 'Unable to process'
        }), 422

    @app.errorhandler(AuthError)
    def Auth_Error(e):
        return jsonify({
            "success": False,
            "error": e.status_code,
            "message": e.error['description']
        }), e.status_code

    return app


app = create_app()
if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
