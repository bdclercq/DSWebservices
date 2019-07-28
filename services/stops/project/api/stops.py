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


@stops_blueprint.route('/stops/get_lines/<prov>', methods=['POST', 'GET'])
def get_lines(prov):
    conn = http.client.HTTPSConnection('delijn.azure-api.net')
    conn.request("GET", "/DLKernOpenData/api/v1/entiteiten/{0}/lijnen".format(prov), "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    data = json.loads(data)
    response_object = {
        'status': 'success',
        'data': {
            'lines': [line for line in data["lijnen"]]
        }
    }
    return jsonify(response_object), 200


@stops_blueprint.route('/stops/get_stops_line_prov_to/<line>/<prov>', methods=['POST', 'GET'])
def get_stops_line_prov_to(line, prov):
    conn = http.client.HTTPSConnection('delijn.azure-api.net')
    conn.request("GET", "/DLKernOpenData/api/v1/lijnen/{0}/{1}/lijnrichtingen/HEEN/haltes".format(prov, line), "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    data_to = json.loads(data)
    stops = [stop for stop in data_to["haltes"]]
    stopsnrs = [stop["haltenummer"] for stop in stops]
    stopsnrs = list(set(stopsnrs))
    print(stopsnrs)
    response_object = {
        'status': 'success',
        'data': {
            'stops': [stop.to_json() for stop in list(set(db.session.query(Stop).filter(Stop.id.in_(stopsnrs)).all()))]
        }
    }
    return jsonify(response_object), 200


@stops_blueprint.route('/stops/get_stops_line_prov_from/<line>/<prov>', methods=['POST', 'GET'])
def get_stops_line_prov_from(line, prov):
    conn = http.client.HTTPSConnection('delijn.azure-api.net')
    conn.request("GET", "/DLKernOpenData/api/v1/lijnen/{0}/{1}/lijnrichtingen/TERUG/haltes".format(prov, line), "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    data_from = json.loads(data)
    stops = [stop for stop in data_from["haltes"]]
    stopsnrs = [stop["haltenummer"] for stop in stops]
    stopsnrs = list(set(stopsnrs))
    print(stopsnrs)
    response_object = {
        'status': 'success',
        'data': {
            'stops': [stop.to_json() for stop in list(set(db.session.query(Stop).filter(Stop.id.in_(stopsnrs)).all()))]
        }
    }
    return jsonify(response_object), 200


@stops_blueprint.route('/', methods=['GET', 'POST'])
def index():
    stops = list(set(Stop.query.all()))
    return render_template('index.html', stops=stops)
