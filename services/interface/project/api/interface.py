from flask import Blueprint, jsonify, request, render_template, redirect
import requests
import json

UI_blueprint = Blueprint('interface', __name__, template_folder='./templates')


@UI_blueprint.route('/', methods=['GET', 'POST'])
def index():
    usrs = requests.get("http://users:5001/get_users")
    return render_template('index.html', users=usrs.json()['data']['users'])

################################################################


@UI_blueprint.route('/Users', methods=['GET'])
def user_management():
    usrs = requests.get("http://users:5001/get_users")
    return render_template("users.html", users=usrs.json()['data']['users'])


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

################################################################


@UI_blueprint.route('/Vehicles', methods=['GET', 'POST'])
def vehicle_management():
    vehicles = requests.get("http://vehicles:5004/vehicles")
    return render_template("vehicles.html", vehicles=vehicles.json()['data']['vehicles'])


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

################################################################


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

################################################################


@UI_blueprint.route('/Stops', methods=['POST', 'GET'])
def stops_management():
    stops = requests.get("http://stops:5003/stops")
    return render_template("stops.html", stops=stops.json()['data']['stops'])


@UI_blueprint.route("/view_stops", methods=['POST', 'GET'])
def view_all_stops():
    stops = requests.get("http://stops:5003/stops")
    return render_template("view_stops.html", stops=stops.json()['data']['stops'])


@UI_blueprint.route("/view_stops_provinces", methods=['POST', 'GET'])
def view_stops_provinces():
    provs = requests.get("http://stops:5003/stops/getProvs")
    return render_template("view_stops_provinces.html", provs=provs.json()['data']['provinces'])


@UI_blueprint.route("/view_stops_province/<prov>", methods=['POST', 'GET'])
def view_stops_province(prov):
    stops = requests.get("http://stops:5003/stops/get_prov/{0}".format(prov))
    return render_template("view_stops.html", stops=stops.json()['data']['stops'])


@UI_blueprint.route('/view_stops_lines', methods=['POST', 'GET'])
def view_stops_lines():
    provs = requests.get("http://stops:5003/stops/getProvs")
    return render_template("view_stops_lines.html", provs=provs.json()['data']['provinces'])


@UI_blueprint.route('/view_lines/<prov>', methods=['POST', 'GET'])
def view_lines(prov):
    lines = requests.get("http://stops:5003/stops/get_lines/{0}".format(prov))
    provs = requests.get("http://stops:5003/stops/getProvs")
    prov_name = 0
    for p in provs.json()['data']['provinces']:
        if p['entiteitnummer'] == prov:
            prov_name = p['omschrijving']
    return render_template("view_lines.html", prov=prov, prov_name=prov_name, lines=lines.json()['data']['lines'])


@UI_blueprint.route('/view_stops_line/<prov>/<line>', methods=['POST', 'GET'])
def view_stops_line(prov, line):
    stops_to = requests.get("http://stops:5003/stops/get_stops_line_prov_to/{0}/{1}".format(line, prov))
    stops_from = requests.get("http://stops:5003/stops/get_stops_line_prov_from/{0}/{1}".format(line, prov))
    to_stops = stops_to.json()['data']['stops']
    from_stops = stops_from.json()['data']['stops']
    if to_stops is None:
        to_stops = []
    if from_stops is None:
        from_stops = []
    return render_template("view_stops.html", stops_to=to_stops, stops_from=from_stops)


# @UI_blueprint.route("/view_stops_locations", methods=['POST', 'GET'])
