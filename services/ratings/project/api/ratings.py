from flask import Blueprint, jsonify, request, render_template
from sqlalchemy import exc
from project.api.models import Rating
from project import db
import requests

ratings_blueprint = Blueprint('ratings', __name__, template_folder='./templates')


@ratings_blueprint.route('/ratings/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@ratings_blueprint.route('/ratings', methods=['POST'])
def add_rating():
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400
    stop_name = post_data.get('stop_name')
    score = post_data.get('score')
    description = post_data.get('description')
    email = post_data.get('email')
    password = post_data.get('password')
    try:
        conn = http.client.HTTPSConnection('https://ratings:5001')
        conn.request("GET", "/ratings/{0},{1}".format(email, password))
        response = conn.getresponse()
        data = response.read()
        conn.close()
        data = json.loads(data)
        if data["status"] == 'success':
            db.session.add(Rating(stop_name=stop_name, score=score, description=description))
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = f'rating for {stop_name} was added!'
            return jsonify(response_object), 201
        else:
            response_object['message'] = 'Sorry, username/password combo not found.'
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response_object), 400


@ratings_blueprint.route('/ratings', methods=['GET'])
def get_all_ratings():
    """Get all ratings"""
    response_object = {
        'status': 'success',
        'data': {
            'ratings': [rating.to_json() for rating in Rating.query.all()]
        }
    }
    return jsonify(response_object), 200


@ratings_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        stop_name = request.form['stop_name']
        score = request.form['score']
        description = request.form['description']
        db.session.add(Rating(stop_name=stop_name, score=score, description=description))
        db.session.commit()
    ratings = Rating.query.all()
    response = requests.get('http://stops:5000/stops')
    data = response.json()
    return render_template('index.html', ratings=ratings, stops=data)
