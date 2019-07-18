from flask import Blueprint, jsonify, request, render_template, redirect
import requests
import json

UI_blueprint = Blueprint('interface', __name__, template_folder='./templates')


@UI_blueprint.route('/', methods=['GET', 'POST'])
def index():
    usrs = requests.get("http://users:5001/get_users")
    return render_template('index.html', users=usrs)


@UI_blueprint.route('/Users', methods=['GET'])
def user_management():
    usrs = requests.get("http://users:5001/get_users")
    return render_template("users.html", users=usrs)


@UI_blueprint.route('/Vehicles', methods=['GET', 'POST'])
def vehicle_management():
    vehicles = requests.get("http://vehicles:5004/vehicles")
    return render_template("vehicles.html", vehicles=vehicles)


@UI_blueprint.route('/add_user', methods=['POST'])
def add_user():
    result = request.form
    # mail = result['email']
    # pwd = result['pwd']
    # data = json.dumps({'email': mail, 'password': pwd}), 200
    status = requests.post("http://users:5001/add_user", data=result)
    result = json.dumps(status.json())
    # print(result)
    if result[0] == "fail":
        return render_template('users.html', message=result)
    else:
        return render_template('index.html', message=result)


@UI_blueprint.route('/add_vehicle', methods=['POST'])
def add_vehicle():
    result = request.form
    status = requests.post("http://vehicles:5004/add_vehicle", data=result)
    result = json.dumps(status.json())
    if result[0] == "fail":
        return render_template('vehicles.html', message=result)
    else:
        return render_template('index.html', message=result)
