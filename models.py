"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User Model"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    image_url = db.Column(db.String(150), nullable=False, default="/static/avatar-generic.png")
    post_prox = db.relationship("Post")

    def __repr__(self):
        return f"id ={self.id} first_name={self.first_name} last_name={self.last_name} image_url={self.image_url}"

    @property
    def full_name(self):
        """ Return full name """
        return self.first_name + " " + self.last_name


class Post(db.Model):
    """Post Model"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user_prox = db.relationship("User")

    def __repr__(self):
        return f"id ={self.id} title={self.title} content={self.content} created_at={self.created_at} user_id={self.user_id}"
