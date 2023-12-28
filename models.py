"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

default_image_url = "https://icons8.com/icon/tZuAOUGm9AuS/user-default"

class User(db.Model):
    """User"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.Text, nullable = False)
    last_name = db.Column(db.Text, nullable = False)
    image_url = db.Column(db.Text, nullable = False, default = default_image_url)

def connect_db(app):
    """Connect to the database."""

    db.app = app
    db.init_app(app)

