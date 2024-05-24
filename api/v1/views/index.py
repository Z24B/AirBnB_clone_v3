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


classes = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User,
        }


@app_views.route('/status', methods=['GET'])
def get_status():
    """Return the status of the API"""
    return jsonify(status="OK")


@app_views.route("/stats")
def stats():
    """Retrieve the number of each objects by type"""
    statistics = {}

    for key, value in classes.items():
        statistics[key] = storage.count(value)

    return jsonify(statistics)
