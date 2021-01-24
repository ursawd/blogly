"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)
db.create_all()

from flask_debugtoolbar import DebugToolbarExtension

app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config["SECRET_KEY"] = "SECRET!"
debug = DebugToolbarExtension(app)

# Route A
@app.route("/")
def inital_page():
    """Start of routes"""  # TODO: to be addressed later per instructions
    return redirect("/users")


# Route B
@app.route("/users")
def list_users():
    """List Users ordered by last name then first name"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("list-users.html", users=users)


# Route C
@app.route("/users/new")
def add_user_form():
    """Show add user form"""
    return render_template("add-user.html")


# Route D
@app.route("/users/new", methods=["POST"])
def add_user():
    """Add New User"""
    fname = request.form["fname"]
    lname = request.form["lname"]
    # imgurl = request.form["imgurl"]
    # ? ---development ----
    # ? set imgurl to default no matter what the user inputs
    imgurl = "/static/imgs/avatar-generic.png"
    # ? -------------------
    user = User(first_name=fname, last_name=lname, image_url=imgurl)
    db.session.add(user)
    db.session.commit()
    return redirect("/users")


# Route E
@app.route("/users/<int:user_id>")
def detail(user_id):
    """Show user detail"""
    user = User.query.get(user_id)
    return render_template("detail-user.html", user=user)


# Route F
@app.route("/users/<int:user_id>/edit")
def edit_form(user_id):
    """Edit user"""
    # retrieve user record matching passed in id
    user = User.query.get(user_id)

    # display user edit form
    return render_template("edit-user.html", user=user)


# Route G
@app.route("/users/<int:user_id>/edit", methods=["POST"])
def update(user_id):
    """Process user edit form"""
    user = User.query.get(user_id)
    user.first_name = request.form["fname"]
    user.last_name = request.form["lname"]
    user.image_url = request.form["imgurl"]

    db.session.add(user)
    db.session.commit()
    return redirect("/users")


# Route H
@app.route("/users/<int:user_id>/delete")
def delete(user_id):
    """Delete user"""
    # retrieve user record matching passed in id
    user = User.query.get(user_id)
    # match record and delete
    db.session.delete(user)  # uses record (not record id) to delete
    db.session.commit()
    return redirect("/users")


# Route P1
@app.route("/users/<int:user_id>/posts/new")
def new_post_form(user_id):
    """Display new post form"""
    user = User.query.get(user_id)
    return render_template("add-post.html", user=user)


# Route P2
@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def new_post(user_id):
    """Add new post"""
    user = User.query.get(user_id)
    title = request.form["title"]
    content = request.form["content"]
    fk = user_id
    print(">>>>>>>>>>>>>>>", user, flush=True)
    post = Post(title=title, content=content, user_id=fk)
    db.session.add(post)
    db.session.commit()
    return render_template("detail-user.html", user=user)


# Route P3
@app.route("/posts/<int:post_id>")
def show_post_form(post_id):
    """Display post"""
    post = Post.query.get(post_id)
    return render_template("detail-post.html", post=post)


# Route P4
@app.route("/posts/<int:post_id>/edit")
def show_post_edit(post_id):
    """Display post edit form"""
    post = Post.query.get(post_id)
    # display user edit form
    return render_template("edit-post.html", post=post)
