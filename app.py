"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db, User, Post, Tag, PostTag
from datetime import datetime

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


@app.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found(e):
    return render_template("404.html")


# Route A
@app.route("/")
def inital_page():
    """Start of routes / home page"""
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("home.html", posts=posts)


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
    # ? ---development ----
    # ? set imgurl to default no matter what the user inputs
    imgurl = "/static/imgs/avatar-generic.png"
    # imgurl = request.form["imgurl"]
    # ? -------------------
    user = User(first_name=fname, last_name=lname, image_url=imgurl)
    db.session.add(user)
    db.session.commit()
    flash(f"New user added: {user.full_name}")
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
def update_user(user_id):
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
    name = user.full_name
    # match record and delete
    db.session.delete(user)  # uses record (not record id) to delete
    db.session.commit()
    flash(f"User deleted: {name}")
    return redirect("/users")


# Route P1
@app.route("/users/<int:user_id>/posts/new")
def new_post_form(user_id):
    """Display new post form"""
    user = User.query.get(user_id)
    tags = Tag.query.all()
    return render_template("add-post.html", user=user, tags=tags)


# Route P2
@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def new_post(user_id):
    """Add new post"""
    user = User.query.get(user_id)
    title = request.form["title"]
    content = request.form["content"]
    fk = user_id
    tagslist = request.form.getlist("tags-on-post")
    post = Post(title=title, content=content, user_id=fk)
    db.session.add(post)
    db.session.commit()
    # add entry(s) into posts_tags table
    for tagname in tagslist:
        tag = Tag.query.filter_by(name=tagname).first()
        entry = PostTag(post_id=post.id, tag_id=tag.id)
        db.session.add(entry)
    db.session.commit()
    #
    return render_template("detail-user.html", user=user)


# Route P3
@app.route("/posts/<int:post_id>")
def show_post_form(post_id):
    """Display post"""
    post = Post.query.get(post_id)
    tags = post.tags
    return render_template("detail-post.html", post=post, tags=tags)


# Route P4
@app.route("/posts/<int:post_id>/edit")
def show_post_edit(post_id):
    """Display post edit form"""
    post = Post.query.get(post_id)
    tags = Tag.query.all()
    # display user edit form
    return render_template("edit-post.html", post=post, tags=tags)


# Route P5
@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def update_post(post_id):
    """Process post edit form"""
    post = Post.query.get(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]
    db.session.add(post)
    db.session.commit()
    # turn off all tags for post posts_tags table
    cleartags = PostTag.query.filter_by(post_id=post.id).all()
    for entry in cleartags:
        db.session.delete(entry)
    db.session.commit()
    # add current tags to post
    currenttags = request.form.getlist("tagname")  # from html form checkbox(s)
    for tag in currenttags:
        tagfromtable = Tag.query.filter_by(name=tag).first()
        newtag = PostTag(post_id=post.id, tag_id=tagfromtable.id)
        db.session.add(newtag)
    db.session.commit()
    return redirect(f"/posts/{post.id}")


# Route P6
@app.route("/posts/<int:post_id>/delete")
def delete_post(post_id):
    """Delete user"""
    # retrieve user record matching passed in id
    post = Post.query.get(post_id)
    user_id = post.user_prox.id
    # match record and delete
    db.session.delete(post)  # uses record (not record id) to delete
    db.session.commit()
    return redirect(f"/users/{user_id}")


# Route MM1
@app.route("/tags")
def list_tags():
    """Display tags"""
    tags = Tag.query.all()
    return render_template("listtags.html", tags=tags)


# Route MM2
@app.route("/tags/new")
def add_tag():
    """Add a tag"""
    # get posts to display on Create A Tag webform
    posts = Post.query.all()
    return render_template("addtag.html", posts=posts)


# Route MM3
@app.route("/tags/new", methods=["POST"])
def process_add_tag():
    """Process add a tag"""
    # add tag to tags table
    tag = request.form["tagname"]
    tagname = Tag(name=tag)
    db.session.add(tagname)
    db.session.commit()
    # add tag to selected posts (via checkbox)
    selectedposts = request.form.getlist("postfortags")
    for title in selectedposts:
        post = Post.query.filter_by(title=title).first()
        newtag = Tag.query.filter_by(name=tag).first()
        entry = PostTag(post_id=post.id, tag_id=newtag.id)
        db.session.add(entry)
    db.session.commit()
    #
    return redirect("/tags")


# Route MM4
@app.route("/tags/<int:tagid>")
def show_tag(tagid):
    """Show tag info"""
    tag = Tag.query.get(tagid)
    posts = tag.posts
    return render_template("showtag.html", tag=tag, posts=posts)


# Route MM5
@app.route("/tags/<int:tagid>/delete")
def delete_tag(tagid):
    """Delete a tag"""
    # delete tag from tags table
    # automatically deletes entries in PostTag table
    tag = Tag.query.get(tagid)
    db.session.delete(tag)
    db.session.commit()
    return redirect("/tags")


# Route MM6
@app.route("/tags/<int:tagid>/edit")
def show_edit_tag(tagid):
    """show form to edit tag"""
    tag = Tag.query.get(tagid)
    # post w/ selected tag
    posts = Post.query.all()
    return render_template("edittag.html", tag=tag, posts=posts)


# Route MM7
@app.route("/tags/<int:tagid>/edit", methods=["POST"])
def process_edit_tag(tagid):
    """process form to edit tag"""
    # add new tag to db
    tag = Tag.query.get(tagid)
    tag.name = request.form["tagname"]
    db.session.add(tag)
    db.session.commit()
    # remove entry from posts_tags table for all post w/ selected tag
    newtag = Tag.query.get(tagid)
    entries = PostTag.query.filter_by(tag_id=newtag.id).all()
    for entry in entries:
        db.session.delete(entry)
    db.session.commit()
    #
    #
    # make entry for selected posts and selected tag
    titles = request.form.getlist("edit-tag-cb")
    for title in titles:
        post = Post.query.filter_by(title=title).first()
        entrynew = PostTag(post_id=post.id, tag_id=newtag.id)
        db.session.add(entrynew)
        db.session.commit()
    return redirect("/tags")