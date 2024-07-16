from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random


app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def convert_instance_to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "map_url": self.map_url,
            "img_url": self.img_url,
            "location": self.location,
            "amenities": {
                "seats": self.seats,
                "has_toilet": self.has_toilet,
                "has_wifi": self.has_wifi,
                "has_sockets": self.has_sockets,
                "can_take_calls": self.can_take_calls,
                "coffee_price": self.coffee_price,
            }
        }

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read a random Record

@app.route("/random", methods=["GET"])
def get_random_cafe():
    cafes = Cafe.query.all()
    if cafes:
        random_cafe = random.choice(cafes)
        return jsonify(random_cafe.convert_instance_to_dict())
    else:
        return jsonify({"error": "No cafes found"}), 404


# HTTP GET - GET ALLLLL Records:
@app.route("/all", methods=["GET"])
def get_all_cafes():
    all_cafes = Cafe.query.all()
    if all_cafes:
        cafes_list = [cafe.convert_instance_to_dict() for cafe in all_cafes]
        return jsonify(cafes=cafes_list)
    else:
        return jsonify({"error": "No cafes found"}), 404


# HTTP GET - Search Cafe by Location:
@app.route("/searchloca", methods=["GET"])
def search_location():
    # Get the location parameter from the query string
    location_query = request.args.get('location')

    # Ensure the query parameter is not None
    if location_query:
        # Query the database for cafes in the specified location
        cafes = Cafe.query.filter(Cafe.location.ilike(f"%{location_query}%")).all()

        # Check if any cafes were found
        if cafes:
            # Convert the list of cafes to dictionaries
            cafes_list = [cafe.convert_instance_to_dict() for cafe in cafes]

            # Return the list of cafe dictionaries as a JSON response
            return jsonify(cafes=cafes_list)
        else:
            # Return an error message if no cafes were found
            return jsonify({"error": "No cafes found"}), 404
    else:
        # Return an error message if the query parameter is missing
        return jsonify({"error": "Location parameter is missing"}), 400



# HTTP POST - Create Record

# HTTP PUT/PATCH - Update Record

# HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
