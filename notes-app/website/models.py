import datetime

from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

#db model is a blueprint/model stored into certain database (all posts should have same format)
class Post(db.Model):
    #id is automatically set by database software
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    body = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50)) #sports, social, etc.

    # location
    location_city = db.Column(db.String(100))
    location_zip = db.Column(db.String(20))
    location_name = db.Column(db.String(150))

    #days
    event_date = db.Column(db.Date) #single day/start day
    event_day = db.Column(db.String(20)) #day of the week
    event_time = db.Column(db.Time)
    is_recurring = db.Column(db.Boolean, default=False)

    #contact
    instagram_url = db.Column(db.String(300)) #club/event page
    group_chat_url = db.Column(db.String(300)) #group chat access
    contact_email   = db.Column(db.String(150)) #email for who posted

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    #associate post with user
    #foreign key- must pass valid user id (one to many- user to notes)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    #create relationships so tags can be sorted, you can see posts by one user
    author = db.relationship('User', backref='posts')
    tags = db.relationship('Tag', secondary='post_tags', backref='posts')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    #max length is 150, no user has same email
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    #adds post id into user's post relationship (like a list)
    posts = db.relationship('Note')

    #add profile for users
    username = db.Column(db.String(50), unique=True)
    bio = db.Column(db.Text)
    #social links
    instagram_url   = db.Column(db.String(300))
    tiktok_url      = db.Column(db.String(300))
    twitter_url     = db.Column(db.String(300))
    website_url     = db.Column(db.String(300))


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id',  db.Integer, db.ForeignKey('tag.id'))
)