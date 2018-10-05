"""Models for Adoption."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class Pets(db.Model):

    __tablename__ = 'pets'

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(25),nullable=False)
    species = db.Column(db.String(25),nullable=False)
    photo_url = db.Column(db.String(1000),nullable=True)
    age = db.Column(db.Integer,nullable=False)
    notes = db.Column(db.String(25),nullable=True)
    available = db.Column(db.Boolean,nullable=False,default=True)