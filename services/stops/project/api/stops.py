from flask import Blueprint, jsonify, request, render_template
from sqlalchemy import exc
from project.api.models import Stop
from project import db
import http.client
import json

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': 'a80d6af91407478c91c8288afd85452f',
}

stops_blueprint = Blueprint('stops', __name__, template_folder='./templates')


@stops_blueprint.route('/stops', methods=['GET'])
def get_all_stops():
    """Get all stops"""
    response_object = {
        'status': 'success',
        'data': {
            'stops': [stop.to_json() for stop in list(set(Stop.query.all()))]
        }
    }
    return jsonify(response_object), 200


@stops_blueprint.route('/stops/get_loc/<name>', methods=['GET'])
def get_stops_location(name):
    """Get all stops"""
    response_object = {
        'status': 'success',
        'data': {
            'stops': [stop.to_json() for stop in list(set(Stop.query.filter_by(location=name)))]
        }
    }
    return jsonify(response_object), 200


@stops_blueprint.route('/stops/get_prov/<prov>', methods=['GET'])
def get_stops_province(prov):
    """Get all stops"""
    response_object = {
        'status': 'success',
        'data': {
            'stops': [stop.to_json() for stop in list(set(Stop.query.filter_by(province=prov)))]
        }
    }
    return jsonify(response_object), 200


@stops_blueprint.route('/stops/getProvs', methods=['POST', 'GET'])
def getProvs():
    conn = http.client.HTTPSConnection('delijn.azure-api.net')
    conn.request("GET", "/DLKernOpenData/api/v1/entiteiten", "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    data = json.loads(data)
    response_object = {
        'status': 'success',
        'data': {
            'provinces': [prov for prov in data["entiteiten"]]
        }
    }
    return jsonify(response_object), 200


@stops_blueprint.route('/', methods=['GET', 'POST'])
def index():
    stops = list(set(Stop.query.all()))
    return render_template('index.html', stops=stops)
