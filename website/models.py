from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String)
    data = db.Column(db.String)
    createdDate = db.Column(db.DateTime(timezone=True), default=func.now())
    misc = db.Column(db.String)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(250))
    joinedDate = db.Column(db.DateTime(timezone=True), default=func.now())
    book = db.relationship('Book')
    misc = db.Column(db.String)
