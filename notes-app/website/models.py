from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

#db model is a blueprint/model stored into certain database (all notes should look the same)
class Note(db.Model):
    #id is automatically set by database software
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    #associate note with user
    #foreign key- must pass valid user id (one to many- user to notes)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    #max length is 150, no user has same email
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    #adds note id into user's note relationship (like a list)
    notes = db.relationship('Note')