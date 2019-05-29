from flask import Blueprint, jsonify, request, render_template, redirect
import requests

UI_blueprint = Blueprint('interface', __name__, template_folder='./templates')


@UI_blueprint.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@UI_blueprint.route('/Users', methods=['GET'])
def user_management():
    return render_template("users.html")

@UI_blueprint.route('/add_user', methods=['POST'])
def add_user():
    result = request.form
    mail = result['email']
    pwd = result['pwd']
    status = requests.post(app.config["USERS_URI"] + "/add_user", json={'email': mail, 'password': pwd})
    result = status.json()
    if result["status"] == "fail":
        return render_template('users.html', message=result['message'])
    else:
        return render_template('index.html', message="User has been added.")