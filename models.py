"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)


class PostTag(db.Model):
    """Intermediate table to join posts and tags"""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)


class Tag(db.Model):
    """Tag Model"""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    posts = db.relationship("Post", secondary="posts_tags", backref="tags")

    def __repr__(self):
        return f"Name = {self.name}"


class User(db.Model):
    """User Model"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    image_url = db.Column(db.String(150), nullable=False, default="/static/imgs/avatar-generic.png")
    post_prox = db.relationship("Post", cascade="all, delete")

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
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user_prox = db.relationship("User")

    def __repr__(self):
        return f"id ={self.id} title={self.title} content={self.content} created_at={self.created_at} user_id={self.user_id}"

    @property
    def friendly_date(self):
        """ Return formated date time """
        return self.created_at.strftime("%b %d, %Y, %I:%M %p")