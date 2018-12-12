from flask import Blueprint, jsonify, request, render_template
from sqlalchemy import exc
from project.api.models import Stop
from project import db

stops_blueprint = Blueprint('stops', __name__, template_folder='./templates')


@stops_blueprint.route('/stops/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


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


@stops_blueprint.route('/', methods=['GET', 'POST'])
def index():
    stops = list(set(Stop.query.all()))
    return render_template('index.html', stops=stops)
