#!/usr/bin/python3
"""User object that handles all default RESTFul API actions"""
from flask import Flask, jsonify, request, abort
from models import storage
from models.user import User
from api.v1.views import app_views


# Route to retrieve all users
@app_views.route('/users', methods=['GET'])
def get_users():
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)


# Route to retrieve a specific user
@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


# Route to delete a user
@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


# Route to create a user
@app_views.route('/users', methods=['POST'])
def create_user():
    if not request.is_json:
        abort(400, description='Not a JSON')
    data = request.get_json()
    if 'email' not in data:
        abort(400, description='Missing email')
    if 'password' not in data:
        abort(400, description='Missing password')
    user = User(**data)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


# Route to update a user
@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.is_json:
        abort(400, description='Not a JSON')
    data = request.get_json()
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
