from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .models import db, User, Place

bp = Blueprint('api', __name__)

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token)
    return jsonify({"message": "Invalid credentials"}), 401

@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({"message": "User logged out successfully"})

@bp.route('/places', methods=['POST'])
@jwt_required()
def add_place():
    user_id = get_jwt_identity()
    data = request.get_json()
    place = Place(user_id=user_id, name=data['name'], description=data['description'], location=data['location'], visited_on=data['visited_on'])
    db.session.add(place)
    db.session.commit()
    return jsonify({"message": "Place added successfully"}), 201

@bp.route('/places', methods=['GET'])
@jwt_required()
def get_places():
    user_id = get_jwt_identity()
    places = Place.query.filter_by(user_id=user_id).all()
    return jsonify([{"id": place.id, "name": place.name, "description": place.description, "location": place.location, "visited_on": place.visited_on} for place in places]), 200

@bp.route('/places/<int:id>', methods=['GET'])
@jwt_required()
def get_place(id):
    user_id = get_jwt_identity()
    place = Place.query.filter_by(id=id, user_id=user_id).first_or_404()
    return jsonify({"id": place.id, "name": place.name, "description": place.description, "location": place.location, "visited_on": place.visited_on}), 200

@bp.route('/places/<int:id>', methods=['PUT'])
@jwt_required()
def update_place(id):
    user_id = get_jwt_identity()
    place = Place.query.filter_by(id=id, user_id=user_id).first_or_404()
    data = request.get_json()
    place.name = data.get('name', place.name)
    place.description = data.get('description', place.description)
    place.location = data.get('location', place.location)
    place.visited_on = data.get('visited_on', place.visited_on)
    db.session.commit()
    return jsonify({"message": "Place updated successfully"}), 200

@bp.route('/places/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_place(id):
    user_id = get_jwt_identity()
    place = Place.query.filter_by(id=id, user_id=user_id).first_or_404()
    db.session.delete(place)
    db.session.commit()
    return jsonify({"message": "Place deleted successfully"}), 204
