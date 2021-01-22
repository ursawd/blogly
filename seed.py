"""Seed file to make sample data for db."""

from models import db, User
from app import app

# Create all tables
db.drop_all()
db.create_all()

phil = User(first_name="Philip", last_name="Bailey", image_url="/static/avatar-generic.png")
jason = User(first_name="Jason", last_name="Stone", image_url="/static/pic1.jfif")
john = User(first_name="John", last_name="Doe", image_url="/static/avatar-generic.png")
jane = User(first_name="Jane", last_name="Doe", image_url="/static/jane.jpg")

db.session.add(phil)
db.session.add(john)
db.session.add(jane)
db.session.add(jason)

db.session.commit()
