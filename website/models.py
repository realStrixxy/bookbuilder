from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(1000))
    data = db.Column(db.String(1000000))
    createdDate = db.Column(db.DateTime(timezone=True), default=func.now())
    misc = db.Column(db.String(1000000))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(20))
    joinedDate = db.Column(db.DateTime(timezone=True), default=func.now())
    book = db.relationship('Book')
    misc = db.Column(db.String(1000000))