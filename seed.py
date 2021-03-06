"""Seed file to make sample data for db."""

from models import db, User, Post, Tag, PostTag
from app import app

# Create all tables
db.drop_all()
db.create_all()

# create 2 tags
tag1 = Tag(name="Tag1Name")
tag2 = Tag(name="Tag2Name")
db.session.add(tag1)
db.session.add(tag2)
db.session.commit()

# create 4 users
phil = User(first_name="Philip", last_name="Bailey", image_url="/static/imgs/avatar-generic.png")
jason = User(first_name="Jason", last_name="Stone", image_url="/static/imgs/pic1.jfif")
john = User(first_name="John", last_name="Doe", image_url="/static/imgs/avatar-generic.png")
jane = User(first_name="Jane", last_name="Doe", image_url="/static/imgs/jane.jpg")

db.session.add(phil)
db.session.add(john)
db.session.add(jane)
db.session.add(jason)
db.session.commit()

# create 2 posts
post1 = Post(
    title="Title of Post # 1",
    content="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec nec urna ac mi consequat tincidunt sed sed eros. Cras sit amet mi in enim dictum ultrices at sit amet nisi.",
    user_id="1",
)
post2 = Post(
    title="Title of Post # 2",
    content="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec nec urna ac mi consequat tincidunt sed sed eros. Cras sit amet mi in enim dictum ultrices at sit amet nisi.",
    user_id="1",
)
db.session.add(post1)
db.session.add(post2)
db.session.commit()

pt1 = PostTag(post_id=1, tag_id=1)
pt2 = PostTag(post_id=1, tag_id=2)
pt3 = PostTag(post_id=2, tag_id=1)
db.session.add_all([pt1, pt2, pt3])
db.session.commit()