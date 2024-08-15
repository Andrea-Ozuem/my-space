#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Tasks """

from flask import abort, jsonify, make_response, request

from models.user import User
from models.tasks import Tasks
from models import storage
from api.v1.views import app_views
from api.v1.auth.middleware import token_required


@app_views.route('/me/tasks', methods=['GET'],
                 strict_slashes=False)
@token_required
def get_tasks(current_user: User):
    """
    Retrieves the list of all tasks objects
    of a specific User, or a specific task
    """
    list_tasks = []
    if not current_user:
        abort(404)
    for task in current_user.tasks:
        list_tasks.append(task.to_dict())
    return jsonify(list_tasks)


@app_views.route('/me/tasks', methods=['POST'],
                 strict_slashes=False)
@token_required
def post_task(current_user: User):
    """
    Creates a Task for a particular User
    """
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'description' not in request.get_json():
        abort(400, description="Missing description")
    data = request.get_json()
    instance = Tasks(**data)
    instance.user_id = current_user.id
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/tasks/<task_id>', methods=['GET'], strict_slashes=False)
@token_required
def get_task(current_user: User, task_id):
    """
    Retrieves a specific task based on id
    """
    task = storage.get(Tasks, task_id)
    if not task:
        abort(404)
    return jsonify(task.to_dict())


@app_views.route('/tasks/<task_id>', methods=['PUT'], strict_slashes=False)
@token_required
def put_task(current_user: User, task_id):
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
@token_required
def delete_task(current_user: User, task_id):
    """
    Deletes a task based on id provided
    """
    task = storage.get(Tasks, task_id)

    if not task:
        abort(404)
    storage.delete(task)
    storage.save()

    return make_response(jsonify({}), 204)


@app_views.route('/tasks/clear', methods=['DELETE'], strict_slashes=False)
@token_required
def clear_completed(current_user: User):
    '''Deletes all completed task of a looged in user'''
    storage.clear_completed(Tasks)
    return make_response(jsonify({}), 204)
