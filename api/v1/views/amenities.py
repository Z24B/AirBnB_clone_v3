#!/usr/bin/python3
"""Amenity objects that handles all default RESTFul API actions"""
from flask import Flask, jsonify, request, abort
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


# Route to retrieve all amenities
@app_views.route('/amenities', methods=['GET'])
def get_amenities():
    amenities = [amenity.to_dict() for amenity in storage.all(
        Amenity).values()]
    return jsonify(amenities)


# Route to retrieve a specific amenity
@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


# Route to delete an amenity
@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


# Route to create an amenity
@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    if not request.is_json:
        abort(400, description='Not a JSON')
    data = request.get_json()
    if 'name' not in data:
        abort(400, description='Missing name')
    amenity = Amenity(**data)
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


# Route to update an amenity
@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not request.is_json:
        abort(400, description='Not a JSON')
    data = request.get_json()
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
