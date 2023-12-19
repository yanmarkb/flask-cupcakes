"""Flask app for Cupcakes"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify  # Importing the Flask class, render_template function, and request object.

from flask_debugtoolbar import DebugToolbarExtension

from models import db, Cupcake, connect_db

app = Flask(__name__)  # Creating an instance of the Flask class.

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'  # Configuring the database URI.

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disabling modification tracking.

app.config['SQLALCHEMY_ECHO'] = True  # Enabling SQL query logging.

app.config['SECRET_KEY'] = 'super-secret-key'  # Setting the secret key for the session.

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

db.init_app(app)  # Initializing the database with the Flask application.

@app.before_first_request  # A decorator that runs the decorated function before the first request to the application.
def create_tables():
    db.create_all()  # Creating all the database tables.
    cupcake = Cupcake(flavor="TestFlavor", size="TestSize", rating=5, image="http://test.com/cupcake.jpg")
    db.session.add(cupcake)
    db.session.commit()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/cupcakes', methods=['GET'])
def get_all_cupcakes():
    cupcakes = Cupcake.query.all()
    response_body = {
        'cupcakes': [cupcake.to_dict() for cupcake in cupcakes]
    }
    return jsonify(response_body)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['GET'])
def get_single_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    response_body = {
        'cupcake': cupcake.to_dict()
    }
    return jsonify(response_body)

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    if request.json is None:
        return jsonify(error="No JSON data provided"), 400

    new_cupcake = Cupcake(
        flavor=request.json.get('flavor'),
        size=request.json.get('size'),
        rating=request.json.get('rating'),
        image=request.json.get('image', "https://tinyurl.com/demo-cupcake")
    )
    db.session.add(new_cupcake)
    db.session.commit()
    response_body = {
        'cupcake': new_cupcake.to_dict()
    }
    return (jsonify(response_body), 201)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    if request.json is not None:
        cupcake.flavor = request.json.get('flavor', cupcake.flavor)
        cupcake.size = request.json.get('size', cupcake.size)
        cupcake.rating = request.json.get('rating', cupcake.rating)
        cupcake.image = request.json.get('image', cupcake.image)
    else:
        return jsonify(error="No JSON data provided"), 400

    db.session.commit()

    return jsonify(cupcake=cupcake.to_dict()), 200

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted"), 200