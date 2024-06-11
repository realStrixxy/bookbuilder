from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.Text)
    data = db.Column(db.Text)
    createdDate = db.Column(db.DateTime(timezone=True), default=func.now())
    misc = db.Column(db.Text)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)
    joinedDate = db.Column(db.DateTime(timezone=True), default=func.now())
    book = db.relationship('Book')
    misc = db.Column(db.Text)