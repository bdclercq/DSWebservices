from flask import Blueprint, jsonify, request, render_template
from sqlalchemy import exc
from project.api.models import Rating
from project import db
import requests

ratings_blueprint = Blueprint('ratings', __name__, template_folder='./templates')


@ratings_blueprint.route('/rate_vehicle', methods=['POST'])
def rate_vehicle():
    print("Rating a vehicl")
    post_data = request.form
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400
    number = post_data['number']
    score = post_data['score']
    description = post_data['descr']
    email = post_data['email']
    password = post_data['password']
    print("Rating for ", number)
    try:
        vehicle_status = requests.get("http://vehicles:5004/check_exists/{0}".format(number))
        vehicle_data = vehicle_status.json()
        user_status = requests.get("http://users:5001/authenticate/{0},{1}".format(email, password))
        user_data = user_status.json()
        if vehicle_data["status"] == 'success' and user_data['status'] == 'success':
            print("Authentication success and vehicle exists")
            db.session.add(Rating(rating_for=str(number), score=float(score), description=description))
            db.session.commit()
            vhs = db.session.query(Rating).filter_by(rating_for=str(number)).all()
            sum = 0.0
            for vh in vhs:
                sum += vh.score
            avg_rating = sum/float(len(vhs))
            update_status = requests.post("http://vehicles:5004/update_score/{0}/{1}".format(number, avg_rating))
            update_data = update_status.json()
            if update_data['status'] == 'success':
                response_object['status'] = 'success'
                response_object['message'] = f'rating for {str(number)} was added!'
                return jsonify(response_object), 201
        else:
            response_object['message'] = 'Sorry, username/password combo or vehicle not found.'
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response_object), 400


@ratings_blueprint.route('/ratings', methods=['GET'])
def get_all_ratings():
    """Get all ratings"""
    response_object = {
        'status': 'success',
        'data': {
            'ratings': [rating.to_json() for rating in Rating.query.all()]
        }
    }
    return jsonify(response_object), 200


