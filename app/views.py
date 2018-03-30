import os, random
from app import app
from flask import abort, Flask, jsonify, make_response, request
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)
from .app_class import WeConnect

app.config['JWT_SECRET_KEY'] = os.urandom(20)
jwt = JWTManager(app)

weconnect = Connect()

@app.route('/api/v1/auth/register', methods=['POST'])
def register_user():
    data = request.get_json()
    email = data['email']
    first_name = data['first_name']
    last_name = data['last_name']
    password = data['password']
    if not data or not email:
        abort(400)
    if email is None:
        abort(400)
    new_user = weconnect.register_user(random.randint(1, 500),
                                      first_name, last_name, email, password)
    if new_user:
        return jsonify({'message': 'Successfully created user'}), 200

@app.route('/api/v1/auth/login', methods=['POST'])
def login_user():
    data = request.get_json()
    email = data['email']
    password = data['password']
    if not data or not email:
        abort(400)
    user = weconnect.login_user(email, password)
    if user:
        access_token = create_access_token(identity=user)
        return jsonify(access_token=access_token), 200
    else:
        abort(404)

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    pass


@app.route('/api/v1/auth/reset-password', methods=['POST'])
@jwt_required
def reset_password():
    data = request.get_json()
    email = data['email']
    password = data['password']
    new_password = data['new_password']
    if not data or not email or not password or not new_password:
        return jsonify({'message': 'Supply your password and/or a new password'}), 401
    user = weconnect.reset_password(email, password, new_password)
    if user:
        return jsonify({'message': 'Successfully updated password'}), 200
    else:
        return jsonify({'message': 'Supply your password and/or a new password'}), 401

@app.route('/api/v1/businesses', methods=['GET'])
@jwt_required
def get_businesses():
    """Returns all businesses"""
    businesses = weconnect.get_businesses()
    return jsonify({'businesses': businesses})


@app.route('/api/v1/businesses/<businessId>', methods=['GET'])
@jwt_required
def get_business(businessId):
    """Returns a specific business"""
    business = weconnect.get_business(int(businessId))
    if business is None:
        abort(404)
    return jsonify({'business': business})


@app.route('/api/v1/businesses', methods=['POST'])
@jwt_required
def register_business():
    """Registers a business"""
    data = request.get_json()
    name = data['name']
    location = data['location']
    description = data['description']
    category = data['category']
    current_user = get_jwt_identity()
    user_id = current_user
    if not data or not name:
        abort(400)
    if name is not None or description is not None or location is not None or category is not None:
        new_business = weconnect.create_business(user_id, random.randint(1, 500), name, location, category, description)
        return jsonify({'business': new_business}), 201
    return jsonify({"response": "Empty value entered"}), 400

@app.route('/api/v1/businesses/<businessId>', methods=['PUT'])
@jwt_required
def update_business(businessId):
    """Updates a business"""
    if int(businessId) == 0:
        abort(404)
    data = request.get_json()
    name = data['name']
    location = data['location']
    description = data['description']
    category = data['category']
    current_user = get_jwt_identity()
    user_id = current_user
    if not data:
        abort(400)
    if name and isinstance(name, str) == False:
        abort(400)
    if description and isinstance(name, str) == False:
        abort(400)
    if location and isinstance(location, str) == False:
        abort(400)
    if category and isinstance(category, str) == False:
        abort(400)

    if name or description or location or category is not None:
        business = weconnect.update_business(user_id, int(businessId), name, location, description, category)
        return jsonify(business), 201

