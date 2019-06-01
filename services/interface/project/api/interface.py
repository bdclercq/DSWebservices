from flask import Blueprint, jsonify, request, render_template, redirect
import requests
import json

UI_blueprint = Blueprint('interface', __name__, template_folder='./templates')


@UI_blueprint.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@UI_blueprint.route('/Users', methods=['GET'])
def user_management():
    usrs = requests.get("http://users:5001/get_users")
    return render_template("users.html")

@UI_blueprint.route('/add_user', methods=['POST'])
def add_user():
    result = request.form
    mail = result['email']
    pwd = result['pwd']
    data = json.dumps({'email': mail, 'password': pwd}), 200
    status = requests.post("http://users:5001/add_user", json=data)
    result = json.dumps(status.json())
    if result["status"] == "fail":
        return render_template('users.html', message=result['message'])
    else:
        return render_template('index.html', message="User has been added.")