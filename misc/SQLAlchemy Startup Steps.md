# SQLAlchemy Startup Steps

## Initialization

- ### In venv

  - `pip install psycopg2-binary`
  - `pip install flask-sqlalchemy`

- ### For checking model, etc.

  - (venv) λ: ipython
  - In[1]: %run app.py

## App (app.py)

    from flask import Flask, request, redirect, render_template
    from models import db, connect_db, Pet

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///db_name"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = True

    connect_db(app)

    from flask_debugtoolbar import DebugToolbarExtension
    app.config["SECRET_KEY"] = "SECRET!"
    debug = DebugToolbarExtension(app)

    @app.route("/")
    def list_pets():
      """List pets and show add form."""
      pets = Pet.query.all()
      return render_template("list.html", pets=pets)

    @app.route("/", methods=["POST"])
    def add_pet():
      """Add pet and redirect to list."""
      name = request.form["name"]
      species = request.form["species"]
      hunger = request.form["hunger"]
      hunger = int(hunger) if hunger else None

      pet = Pet(name=name, species=species, hunger=hunger)
      db.session.add(pet)
      db.session.commit()

      return redirect(f"/{pet.id}")

    @app.route("/<int:pet_id>")
    def show_pet(pet_id):
      """Show info on a single pet."""
      pet = Pet.query.get_or_404(pet_id)
      return render_template("detail.html", pet=pet)`

## Models (models.py)

    from flask_sqlalchemy import SQLAlchemy
    db = SQLAlchemy()

    def connect_db(app):
    """Connect to database."""
      db.app = app
      db.init_app(app)

    class Pet(db.Model):
      """Pet."""

      __tablename__ = "pets"

      id = db.Column(db.Integer, primary_key=True, autoincrement=True)
      name = db.Column(db.String(50), nullable=False, unique=True)
      species = db.Column(db.String(30), nullable=True)
      hunger = db.Column(db.Integer, nullable=False, default=20)

    def greet(self):
        """Greet using name."""

        return f"I'm {self.name} the {self.species or 'thing'}"

    def feed(self, units=10):
        """Nom nom nom."""

        self.hunger -= units
        self.hunger = max(self.hunger, 0)

    def __repr__(self):
        """Show info about pet."""

        p = self
        return f"<Pet {p.id} {p.name} {p.species} {p.hunger}>"

    @classmethod
    def get_by_species(cls, species):
        """Get all pets matching that species."""

        return cls.query.filter_by(species=species).all()
