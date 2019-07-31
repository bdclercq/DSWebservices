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
            db.session.add(Rating(rating_for=str(number), score=float(score), description=description, rating_type=0,
                                  rated_by=email))
            db.session.commit()
            vhs = db.session.query(Rating).filter_by(rating_for=str(number), rating_type=0).all()
            sum = 0.0
            for vh in vhs:
                sum += vh.score
            avg_rating = sum/float(len(vhs))
            update_status = requests.post("http://vehicles:5004/update_score/{0}/{1}".format(number, avg_rating))
            update_data = update_status.json()
            if update_data['status'] == 'success':
                response_object['status'] = 'success'
                response_object['message'] = 'Rating was added!'
                return jsonify(response_object), 201
        else:
            response_object['message'] = 'Sorry, username/password combo or vehicle not found.'
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response_object), 400


@ratings_blueprint.route('/rate_stop', methods=['POST'])
def rate_stop():
    print("Rating a stop")
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
        stop_status = requests.get("http://stops:5003/check_exists/{0}".format(number))
        stop_data = stop_status.json()
        user_status = requests.get("http://users:5001/authenticate/{0},{1}".format(email, password))
        user_data = user_status.json()
        if stop_data["status"] == 'success' and user_data['status'] == 'success':
            print("Authentication success and stop exists")
            db.session.add(Rating(rating_for=str(number), score=float(score), description=description, rating_type=1,
                                  rated_by=email))
            db.session.commit()
            stops = db.session.query(Rating).filter_by(rating_for=str(number), rating_type=1).all()
            sum = 0.0
            for stop in stops:
                sum += stop.score
            avg_rating = sum/float(len(stops))
            update_status = requests.post("http://stops:5003/update_score/{0}/{1}".format(number, avg_rating))
            update_data = update_status.json()
            if update_data['status'] == 'success':
                response_object['status'] = 'success'
                response_object['message'] = 'Rating was added!'
                return jsonify(response_object), 201
        else:
            response_object['message'] = 'Sorry, username/password combo or vehicle not found.'
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response_object), 400


@ratings_blueprint.route('/ratings/<rfor>/<rtype>', methods=['GET'])
def ratings(rfor, rtype):
    response_object = {
        'status': 'success',
        'data': {
            'ratings': [rating.to_json() for rating in
                        list(set(Rating.query.filter_by(rating_for=rfor, rating_type=rtype)))]
        }
    }
    return jsonify(response_object), 200


@ratings_blueprint.route('/ratings/remove/<rfor>/<rtype>', methods=['GET'])
def remove(rfor, rtype):
    response_object = {
        'status': 'success',
        'data': {
            'message': 'Ratings were removed successfully.'
        }
    }
    ratings = db.session.query(Rating).filter_by(rating_for=rfor, rating_type=rtype).all()
    if len(ratings) >= 1:
        try:
            for rating in ratings:
                db.session.delete(rating)
                db.session.commit()
        except:
            response_object['status'] = 'fail'
            response_object['message'] = 'Cannot remove ratings.'
    else:
        response_object['message'] = 'No ratings to remove.'
    return jsonify(response_object), 200


