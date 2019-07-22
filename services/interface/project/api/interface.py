from flask import Blueprint, jsonify, request, render_template, redirect
import requests
import json

UI_blueprint = Blueprint('interface', __name__, template_folder='./templates')


@UI_blueprint.route('/', methods=['GET', 'POST'])
def index():
    usrs = requests.get("http://users:5001/get_users")
    return render_template('index.html', users=usrs.json()['data']['users'])


@UI_blueprint.route('/Users', methods=['GET'])
def user_management():
    usrs = requests.get("http://users:5001/get_users")
    return render_template("users.html", users=usrs.json()['data']['users'])


@UI_blueprint.route('/Vehicles', methods=['GET', 'POST'])
def vehicle_management():
    vehicles = requests.get("http://vehicles:5004/vehicles")
    return render_template("vehicles.html", vehicles=vehicles.json()['data']['vehicles'])


@UI_blueprint.route('/add_user', methods=['POST'])
def add_user():
    result = request.form
    # mail = result['email']
    # pwd = result['pwd']
    # data = json.dumps({'email': mail, 'password': pwd}), 200
    status = requests.post("http://users:5001/add_user", data=result)
    result = status.json()
    # print(result)
    if result['status'] == "fail":
        return render_template('users.html', message=result['message'],
                               users=requests.get("http://users:5001/get_users").json()['data']['users'])
    else:
        return render_template('index.html', message=result['message'],
                               users=requests.get("http://users:5001/get_users").json()['data']['users'])


@UI_blueprint.route('/add_vehicles', methods=['POST', 'GET'])
def add_vehicles():
    return render_template('add_vehicle.html',
                           vehicles=requests.get("http://vehicles:5004/vehicles").json()['data']['vehicles'])


@UI_blueprint.route('/add_vehicle', methods=['POST'])
def add_vehicle():
    result = request.form
    status = requests.post("http://vehicles:5004/add_vehicle", data=result)
    result = status.json()
    if result['status'] == "fail":
        return render_template('vehicles.html', message=result['message'],
                               vehicles=requests.get("http://vehicles:5004/vehicles").json()['data']['vehicles'])
    else:
        return render_template('index.html', message=result['message'],
                               users=requests.get("http://users:5001/get_users").json()['data']['users'])


@UI_blueprint.route('/remove_vehicles', methods=['POST', 'GET'])
def remove_vehicles():
    return render_template('remove_vehicle.html',
                           vehicles=requests.get("http://vehicles:5004/vehicles").json()['data']['vehicles'])


@UI_blueprint.route('/remove_vehicle', methods=['POST'])
def remove_vehicle():
    result = request.form
    status = requests.post("http://vehicles:5004/remove_vehicle", data=result)
    result = status.json()
    if result['status'] == "fail":
        return render_template('vehicles.html', message=result['message'],
                               vehicles=requests.get("http://vehicles:5004/vehicles").json()['data']['vehicles'])
    else:
        return render_template('index.html', message=result['message'],
                               users=requests.get("http://users:5001/get_users").json()['data']['users'])


@UI_blueprint.route('/Ratings', methods=['GET', 'POST'])
def rating_management():
    vehicles = requests.get("http://vehicles:5004/vehicles")
    return render_template("ratings.html", vehicles=vehicles.json()['data']['vehicles'])


@UI_blueprint.route('/rate_vehicles', methods=['POST', 'GET'])
def rate_vehicles():
    return render_template('rate_vehicle.html')


@UI_blueprint.route('/rate_vehicle', methods=['POST', 'GET'])
def rate_vehicle():
    result = request.form
    status = requests.post("http://ratings:5002/rate_vehicle", data=result)
    result = status.json()
    if result['status'] == "fail":
        return render_template('vehicles.html', message=result['message'],
                               vehicles=requests.get("http://vehicles:5004/vehicles").json()['data']['vehicles'])
    else:
        return render_template('index.html', message=result['message'],
                               users=requests.get("http://users:5001/get_users").json()['data']['users'])