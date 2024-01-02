"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

db = SQLAlchemy()

default_image_url = "https://img.icons8.com/?size=256&id=tZuAOUGm9AuS&format=png"

class User(db.Model):
    """User"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.Text, nullable = False)
    last_name = db.Column(db.Text, nullable = False)
    image_url = db.Column(db.Text, nullable = False, default = default_image_url)

class Post(db.Model):
    """Post"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', backref='posts')
    tags = db.relationship('Tag', secondary='post_tags')

class Tag(db.Model):
    """Tag"""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)

    posts = db.relationship('Post', secondary='post_tags')

class PostTag(db.Model):
    __tablename__ = 'post_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

def connect_db(app):
    """Connect to the database."""

    db.app = app
    db.init_app(app)

