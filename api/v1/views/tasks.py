#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Tasks """

from models.user import User
from models.tasks import Tasks
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/users/<user_id>/tasks', methods=['GET'],
                 strict_slashes=False)
def get_tasks(user_id):
    """
    Retrieves the list of all tasks objects
    of a specific User, or a specific task
    """
    list_tasks = []
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    for task in user.tasks:
        list_tasks.append(task.to_dict())

    return jsonify(list_tasks)


@app_views.route('/users/<user_id>/tasks', methods=['POST'],
                 strict_slashes=False)
def post_task(user_id):
    """
    Creates a Task for a particular User
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'description' not in request.get_json():
        abort(400, description="Missing description")
    if 'completed' not in request.get_json():
        abort(400, description="Missing completed")

    data = request.get_json()
    print(type(data))
    instance = Tasks(**data)
    instance.user_id = user.id
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/tasks/<task_id>', methods=['GET'], strict_slashes=False)
def get_task(task_id):
    """
    Retrieves a specific task based on id
    """
    task = storage.get(Tasks, task_id)
    if not task:
        abort(404)
    return jsonify(task.to_dict())


@app_views.route('/tasks/<task_id>', methods=['PUT'], strict_slashes=False)
def put_task(task_id):
    """
    Updates a Task
    """
    task = storage.get(Tasks, task_id)
    if not task:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'user_id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(task, key, value)
    storage.save()
    return make_response(jsonify(task.to_dict()), 200)


@app_views.route('/tasks/<task_id>', methods=['DELETE'], strict_slashes=False)
def delete_task(task_id):
    """
    Deletes a task based on id provided
    """
    task = storage.get(Tasks, task_id)

    if not task:
        abort(404)
    storage.delete(task)
    storage.save()

    return make_response(jsonify({}), 200)
