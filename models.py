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


def connect_db(app):
    """Connect to the database."""

    db.app = app
    db.init_app(app)

