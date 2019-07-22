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
            data = status.json()
            if data['status'] == "success":
                db.session.add(Vehicle(type=type, number=number, creator=email))
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


@vehicles_blueprint.route('/check_exists/<number>', methods=['POST', 'GET'])
def check_exists(number):
    response_object = {
        'status': 'fail',
        'message': 'Vehicle does not exist'
    }
    try:
        exists = Vehicle.query.filter_by(number=number).scalar() is not None
        if not exists:
            return jsonify(response_object), 404
        else:
            response_object['status'] = 'success'
            response_object['message'] = 'Vehicle was found'
            return jsonify(response_object), 200
    except ValueError:
        response_object['message'] = 'An unknown error occurred'
        return jsonify(response_object), 404


@vehicles_blueprint.route('/remove_vehicle', methods=['POST'])
def remove_vehicle():
    post_data = request.form
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400
    number = post_data['number']
    email = post_data['email']
    password = post_data['password']
    try:
        vehicle_exists = db.session.query(Vehicle.number).filter_by(number=number).scalar() is not None
        if vehicle_exists:
            status = requests.get("http://users:5001/authenticate/{0},{1}".format(email, password))
            data = status.json()
            if data['status'] == 'success':
                vehicle = db.session.query(Vehicle).filter_by(number=number).first()
                if vehicle.avg_score == 0.0 and vehicle.creator == email:
                    db.session.delete(vehicle)
                    db.session.commit()
                    response_object['status'] = 'success'
                    response_object['message'] = 'Vehicle was removed'
                    return jsonify(response_object), 201
                else:
                    response_object['message'] = 'The vehicle cannot be removed, it has already been rated or has been added by another user (not you).'
                    return jsonify(response_object), 400
            else:
                response_object['message'] = 'Sorry, username/password combo not found.'
                return jsonify(response_object), 400
        else:
            response_object['message'] = 'Vehicle does not exists.'
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        response_object['message'] = "An error occurred, please try again later."
        return jsonify(response_object), 400


@vehicles_blueprint.route('/update_score/<vid>/<score>', methods=['POST'])
def update_score(vid, score):
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    try:
        vehicle = db.session.query(Vehicle).filter_by(number=vid).first()
        vehicle.avg_score = float(score)
        db.session.commit()
        response_object['status'] = 'success'
        response_object['message'] = 'Score was updated'
        return jsonify(response_object), 201
    except exc.IntegrityError as e:
        db.session.rollback()
        response_object['message'] = "An error occurred, please try again later."
        return jsonify(response_object), 400
