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


@app_views.route('/status', methods=['GET'])
def get_status():
    """Return the status of the API"""
    return jsonify(status="OK")


@app_views.route('/stats', methods=['GET'])
def get_stats():
    """Retrieve the number of each objects by type"""
    classes = {'states': State, 'users': User,
               'amenities': Amenity, 'cities': City,
               'places': Place, 'reviews': Review}
    for key in classes:
        classes[key] = storage.count(classes[key])
    return jsonify(classes)
