from flask import Blueprint, jsonify, request, render_template
from sqlalchemy import exc
from project.api.models import Vehicle
from project import db
import http.client, urllib.request, urllib.parse, urllib.error, base64, json

vehicles_blueprint = Blueprint('vehicles', __name__, template_folder='./templates')


@vehicles_blueprint.route('/add_vehicle', methods=['POST'])
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
    vehicle_exists = Vehicle.query.filter_by(number=number).first().scalar() is not None
    if not vehicle_exists:
        conn = http.client.HTTPSConnection('http://users:5001')
        conn.request("GET", "/authenticate/{0},{1}".format(email, password))
        response = conn.getresponse()
        data = response.read()
        conn.close()
        data = json.loads(data)
        if data['status'] == 'success':
            db.session.add(Vehicle(type=type, number=number, creator=data['data']['id']))
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = 'Vehicle was added'
            return jsonify(response_object), 201
        else:
            response_object['message'] = 'Sorry, username/password combo not found.'
            return jsonify(response_object), 400
    else:
        response_object['message'] = 'Vehicle already exists.'
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


@vehicles_blueprint.route('/remove_vehicle', methods=['POST'])
def remove_vehicle():
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400
    number = post_data.get('number')
    email = post_data.get('email')
    password = post_data.get('password')
    vehicle_exists = Vehicle.query.filter_by(number=number).first().scalar() is not None
    if vehicle_exists:
        conn = http.client.HTTPSConnection('http://users:5001')
        conn.request("GET", "/authenticate/{0},{1}".format(email, password))
        response = conn.getresponse()
        data = response.read()
        conn.close()
        data = json.loads(data)
        if data['status'] == 'success':
            vehicle = Vehicle.query.filter_by(number=number).first()
            if vehicle.avg_score == 0.0:
                db.session.delete(vehicle)
                db.session.commit()
                response_object['status'] = 'success'
                response_object['message'] = 'Vehicle was removed'
                return jsonify(response_object), 201
            else:
                response_object['message'] = 'The vehicle cannot be removed, it has already been rated.'
                return jsonify(response_object), 400
        else:
            response_object['message'] = 'Sorry, username/password combo not found.'
            return jsonify(response_object), 400
    else:
        response_object['message'] = 'Vehicle already exists.'
        return jsonify(response_object), 400



@vehicles_blueprint.route('/', methods=['GET'])
def index():
    vehicles = Vehicle.query.all()
    return render_template('index.html', vehicles=vehicles)
