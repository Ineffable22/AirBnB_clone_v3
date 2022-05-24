#!/usr/bin/python3
"""Create a new view for User objects"""
from models import storage
from models.user import User
from api.v1.views import app_views as views
from flask import jsonify, abort, request
from .utils import get_resource


@views.route('/users', methods=['GET'])
def get_users():
    """Get all stored users"""
    users = storage.all("User").values()
    response = [user.to_dict() for user in users]
    return jsonify(response)


@views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get a User object by id"""
    user = get_resource("User", user_id)
    return jsonify(user.to_dict())


@views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete an User object by its id """
    user = get_resource("User", user_id)
    user.delete()
    storage.save()
    return jsonify({})


@views.route('/users', methods=['POST'])
def insert_user():
    """Insert a new User object"""
    body = get_resource(_req=request)
    if 'email' not in body:
        abort(400, {'message': 'Missing email'})
    if 'password' not in body:
        abort(400, {'message': 'Missing password'})
    new_user = User(**body)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update an User object"""
    [user, body] = get_resource("User", user_id, request)
    for key, value in body.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
