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


# @stops_blueprint.route('/stops/get_loc/<name>', methods=['GET'])
# def get_stops_location(name):
#     """Get all stops"""
#     response_object = {
#         'status': 'success',
#         'data': {
#             'stops': [stop.to_json() for stop in list(set(Stop.query.filter_by(location=name)))]
#         }
#     }
#     return jsonify(response_object), 200


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
    try:
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
    except KeyError as ke:
        # This means that there are no stops for this line in this province
        response_object = {
            'status': 'success',
            'data': {
                'stops': []
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
    try:
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
    except KeyError as ke:
        # This means that there are no stops for this line in this province
        response_object = {
            'status': 'success',
            'data': {
                'stops': []
            }
        }
        return jsonify(response_object), 200


@stops_blueprint.route('/stops/get_locations/<prov>', methods=['POST', 'GET'])
def get_locations(prov):
    conn = http.client.HTTPSConnection('delijn.azure-api.net')
    conn.request("GET", "/DLKernOpenData/api/v1/entiteiten/{0}/gemeenten".format(prov),"{body}", headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    data = json.loads(data)
    locs = [loc for loc in data["gemeenten"]]
    locs = sorted(locs, key=lambda k: k['omschrijving'])
    response_object = {
        'status': 'success',
        'data': {
            'locations': locs
        }
    }
    return jsonify(response_object), 200


@stops_blueprint.route('/stops/get_stops_location/<loc>', methods=['POST', 'GET'])
def get_stops_location(loc):
    conn = http.client.HTTPSConnection('delijn.azure-api.net')
    conn.request("GET", "/DLKernOpenData/api/v1/gemeenten/{0}/haltes".format(loc), "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    data = json.loads(data)
    try:
        stops = [stop for stop in data["haltes"]]
        stopsnrs = [stop["haltenummer"] for stop in stops]
        stopsnrs = list(set(stopsnrs))
        response_object = {
            'status': 'success',
            'data': {
                'stops': [stop.to_json() for stop in
                          list(set(db.session.query(Stop).filter(Stop.id.in_(stopsnrs)).all()))]
            }
        }
        return jsonify(response_object), 200
    except KeyError as ke:
        # This means that there are no stops for this location
        response_object = {
            'status': 'success',
            'data': {
                'stops': []
            }
        }
        return jsonify(response_object), 200


@stops_blueprint.route('/get_name/<id>', methods=['GET', 'POST'])
def get_name(id):
    try:
        stop = db.session.query(Stop).filter(Stop.id==id).first()
        name = stop.stop_name
        response_object = {
            'status': 'success',
            'data': {
                'name': name
            }
        }
        return jsonify(response_object), 200
    except:
        response_object = {
            'status': 'fail',
            'data': {
                'message': "Cannot find stop with that ID."
            }
        }
        return jsonify(response_object), 404


@stops_blueprint.route('/check_exists/<id>', methods=['POST', 'GET'])
def check_exists(id):
    response_object = {
        'status': 'fail',
        'message': 'Vehicle does not exist'
    }
    try:
        exists = Stop.query.filter_by(id=id).scalar() is not None
        if not exists:
            return jsonify(response_object), 404
        else:
            response_object['status'] = 'success'
            response_object['message'] = 'Stop was found'
            return jsonify(response_object), 200
    except ValueError:
        response_object['message'] = 'An unknown error occurred'
        return jsonify(response_object), 404


@stops_blueprint.route('/update_score/<id>/<score>', methods=['POST'])
def update_score(id, score):
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    try:
        stop = db.session.query(Stop).filter_by(id=id).first()
        stop.avg_score = float(score)
        db.session.commit()
        response_object['status'] = 'success'
        response_object['message'] = 'Score was updated'
        return jsonify(response_object), 201
    except exc.IntegrityError as e:
        db.session.rollback()
        response_object['message'] = "An error occurred, please try again later."
        return jsonify(response_object), 400
