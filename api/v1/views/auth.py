#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Tasks """

from models.user import User
from models import storage
from api.v1.views import auth_views
from api.v1.auth.middleware import token_required
from flask import abort, jsonify, make_response, request


@auth_views.route('/register', methods=['POST'], strict_slashes=False)
def register():
    """
    Registers a user
    """
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")

    data = request.get_json()

    if storage.exists(User, data['email']):
        abort(400, description="Email already exists")

    user = User(**data)
    user.password = user.hash_password(data['password'])
    user.save()

    access_token = user.create_access_token(user.id)

    response = jsonify({
        "status_code": 201,
        "message": "User created successfully",
        "data": {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user.to_dict()
        }
    })

    return response, 201


@auth_views.route('/login', methods=['POST'], strict_slashes=False)
def login():
    """
    Logs in a user and generates access token
    """
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")

    data = request.get_json()
    user = storage.exists(User, data['email'])
    if not user:
        abort(400, description="Invalid login credentials")
    if not user.verify_password(data.get('password'), user.password):
        abort(400, description="Invalid login credentials")
    
    access_token = user.create_access_token(user.id)
    response = {
        "status_code": 200,
        "message": "User retrieved successfully",
        "data": {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user.to_dict()
        }
    }

    return jsonify(response), 200