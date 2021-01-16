"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)
db.create_all()

from flask_debugtoolbar import DebugToolbarExtension

app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config["SECRET_KEY"] = "SECRET!"
debug = DebugToolbarExtension(app)


@app.route("/")
def inital_page():
    """Start of routes"""  # TODO: to be addressed later per instructions
    return redirect("/users")


@app.route("/users")
def list_users():
    """List Users"""
    users = User.query.all()
    return render_template("list-users.html", users=users)


@app.route("/add")
def add_user_form():
    """Show add user form"""
    return render_template("add-user.html")


@app.route("/add", methods=["POST"])
def add_user():
    """Add New User"""

    #! redirect?
    return render_template("add-user.html")