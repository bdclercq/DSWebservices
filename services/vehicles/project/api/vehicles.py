from flask import Blueprint, jsonify, request, render_template
from sqlalchemy import exc
from project.api.models import Vehicle
from project import db
import http.client, urllib.request, urllib.parse, urllib.error, base64, json

vehicles_blueprint = Blueprint('vehicles', __name__, template_folder='./templates')


@vehicles_blueprint.route('/vehicles/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@vehicles_blueprint.route('/vehicles', methods=['POST'])
def add_vehicle():
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400
    type = post_data.get('type')
    number = post_data.get('number')
    email = post_data.get('email')
    password = post_data.get('password')
    try:
        vehicle = Vehicle.query.filter_by(number=number).first()
        # user = User.query.filter_by(email=email).first()
        if not vehicle:
            conn = http.client.HTTPSConnection('http://users:5001')
            conn.request("GET", "/users/{0},{1}".format(email, password))
            response = conn.getresponse()
            data = response.read()
            conn.close()
            data = json.loads(data)
            if data['status'] == 'success':
                db.session.add(Vehicle(type=type, number=number))
                db.session.commit()
                response_object['status'] = 'success'
                response_object['message'] = f'A {type} was added!'
                return jsonify(response_object), 201
            else:
                response_object['message'] = 'Sorry, username/password combo not found.'
                return jsonify(response_object), 400
        else:
            response_object['message'] = 'Vehicle already exists.'
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response_object), 400


@vehicles_blueprint.route('/vehicles', methods=['GET'])
def get_all_ratings():
    """Get all vehicles"""
    response_object = {
        'status': 'success',
        'data': {
            'vehicles': [vehicle.to_json() for vehicle in Vehicle.query.all()]
        }
    }
    return jsonify(response_object), 200


@vehicles_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        type = request.form['type']
        number = request.form['number']
        db.session.add(Vehicle(type=type, number=number))
        db.session.commit()
    vehicles = Vehicle.query.all()
    return render_template('index.html', vehicles=vehicles)
