#!/usr/bin/python3
"""Indexing File"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.base_model import BaseModel


@app_views.route('/status', methods=['GET'])
def get_status():
    """Return the status of the API"""
    return jsonify(status="OK")


@app_views.route('/stats', methods=['GET'])
def get_stats():
    """Retrieve the number of each objects by type"""
    stats = {
            "amenities": storage.count("Amenity"),
            "cities": storage.count("City"),
            "places": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User")
            }
    return jsonify(stats)
