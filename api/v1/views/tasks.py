#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Tasks """

from models.user import User
from models.tasks import Tasks
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request

@app_views.route('/users/<user_id>/tasks', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/tasks/<task_id>', methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)