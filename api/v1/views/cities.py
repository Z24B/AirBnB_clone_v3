#!/usr/bin/python3
"""cities"""

from flask import Flask, jsonify, request, abort
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views

# Route to retrieve all cities of a state
@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_state_cities(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)

# Route to retrieve a specific city
@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    return jsonify(city.to_dict())

# Route to delete a city
@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()
    return jsonify({}), 200

# Route to create a city
@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if not request.is_json:
        abort(400, description='Not a JSON')

    data = request.get_json()
    if 'name' not in data:
        abort(400, description='Missing name')

    city = City(**data)
    city.state_id = state_id
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201

# Route to update a city
@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if not request.is_json:
        abort(400, description='Not a JSON')

    data = request.get_json()
    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(city, key, value)

    storage.save()
    return jsonify(city.to_dict()), 200
