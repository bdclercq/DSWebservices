from flask import Blueprint, jsonify, request, render_template
from sqlalchemy import exc
from project.api.models import User
from project import db

users_blueprint = Blueprint('users', __name__, template_folder='./templates')


@users_blueprint.route('/add_user', methods=['POST', 'GET'])
def add_user():
    post_data = request.form
    print(post_data)
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400
    email = post_data['email']
    password = post_data['pwd']
    try:
        user = db.session.query(User.email).filter_by(email=email).scalar() is not None
        if not user:
            db.session.add(User(email=email, password=password))
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = f'{email} was added!'
            return jsonify(response_object), 201
        else:
            response_object['message'] = 'Sorry. That email has already been taken.'
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        response_object['message'] = 'An error occurred, please try again later.'
        return jsonify(response_object), 400


@users_blueprint.route('/authenticate/<email>,<passwd>', methods=['GET'])
def authenticate(email, passwd):
    """Authentication"""
    response_object = {
        'status': 'fail',
        'message': 'User does not exist'
    }
    try:
        exists = User.query.filter_by(email=email, password=passwd).scalar() is not None
        if not exists:
            return jsonify(response_object), 404
        else:
            user = User.query.filter_by(email=email, password=passwd).first()
            response_object = {
                'status': 'success',
                'data': {
                    'id': user.id
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@users_blueprint.route('/get_users', methods=['GET'])
def get_users():
    """Get all users"""
    response_object = {
        'status': 'success',
        'data': {
            'users': [user.to_json() for user in User.query.all()]
        }
    }
    return jsonify(response_object), 200


@users_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db.session.add(User(email=email, password=password))
        db.session.commit()
    users = User.query.all()
    return render_template('index.html', users=users)
