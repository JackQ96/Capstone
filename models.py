from flask_sqlalchemy import SQLAlchemy
from flask import Flask



database_path = 'postgresql://demo1:pass1@localhost/capstone'

app = Flask(__name__)
db = SQLAlchemy()


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

class Movies(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    release_year = db.Column(db.String(5), nullable=False)
    genre = db.Column(db.String(100))

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_year': self.release_year,
            'genre': self.genre
        }

    def insert(self):
        try:
             db.session.add(self)
             db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())


class Actors(db.Model):
    __tablename__='actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(6))
    age = db.Column(db.Integer)

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'age': self.age
        }

    def insert(self):
        try:
             db.session.add(self)
             db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())
    