#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Tasks """

from flask import abort, jsonify, make_response, request

from api.v1.auth.middleware import token_required
from models.user import User
from models import storage
from api.v1.views import app_views

@app_views.route('/users', strict_slashes=False)
@token_required
def get_users(current_user: User):
    """
    Retrieves the list of all user objects
    or a specific user
    """
    all_users = storage.all(User).values()
    list_users = []
    for user in all_users:
        list_users.append(user.to_dict())
    return jsonify(list_users)


@app_views.route('/me', methods=['GET'], strict_slashes=False)
@token_required
def get_current_user(current_user: User):
    """ Retrieves an user """
    return jsonify(current_user.to_dict())


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
@token_required
def get_user(current_user: User, user_id):
    """ Retrieves an user """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
@token_required
def delete_user(current_user: User, user_id):
    """
    Deletes a user Object
    """

    user = storage.get(User, user_id)

    if not user:
        abort(404)

    storage.delete(user)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """
    Creates a user
    """
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")

    data = request.get_json()
    instance = User(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)

@app_views.route('/me/update', methods=['PUT'], strict_slashes=False)
@token_required
def put_user(current_user: User):
    """
    Updates a user
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'email', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(current_user, key, value)
    storage.save()
    return make_response(jsonify(current_user.to_dict()), 200)
