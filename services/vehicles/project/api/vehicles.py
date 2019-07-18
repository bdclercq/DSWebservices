from flask import Blueprint, jsonify, request, render_template
from sqlalchemy import exc
from project.api.models import Vehicle
from project import db
import http.client, urllib.request, urllib.parse, urllib.error, base64, json
import requests

vehicles_blueprint = Blueprint('vehicles', __name__, template_folder='./templates')


@vehicles_blueprint.route('/add_vehicle', methods=['POST', 'GET'])
def add_vehicle():
    post_data = request.form
    print(post_data)
    response_object = {
        'status': 'fail',
        'message': "Invalid payload."
    }
    if not post_data:
        return jsonify(response_object), 400
    type = post_data['type']
    number = post_data['number']
    email = post_data['email']
    password = post_data['password']
    try:
        vehicle_exists = db.session.query(Vehicle.number).filter_by(number=number).scalar() is not None
        if not vehicle_exists:
            status = requests.get("http://users:5001/authenticate/{0},{1}".format(email, password))
            data = json.dumps(status.json())
            print(data[31:38])
            if data[31:38] == "success":
                print("Authentication success")
                db.session.add(Vehicle(id=number, type=type, number=number, creator=email))
                db.session.commit()
                response_object['status'] = 'success'
                response_object['message'] = "Vehicle was added"
                return jsonify(response_object), 201
            else:
                response_object['message'] = "Sorry, username/password combo not found."
                return jsonify(response_object), 400
        else:
            response_object['message'] = "Vehicle already exists."
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        response_object['message'] = "An error occurred, please try again later."
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
