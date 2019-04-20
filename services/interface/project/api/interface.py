from flask import Blueprint, jsonify, request, render_template
from sqlalchemy import exc
from project import db
import requests

UI_blueprint = Blueprint('interface', __name__, template_folder='./templates')


@UI_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        wanted = request.form['wanted']
        return requests.get('http://{0}:5000'.format(wanted))
    return render_template('index.html')
