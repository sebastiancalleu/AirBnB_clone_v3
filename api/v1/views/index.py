#!/usr/bin/python3
""" module to create the routes of the blueprint object """

from api.v1.views import app_views
from flask import jsonify, json, request, make_response
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'])
def jsonresponse():
    """ method to response with a json file """
    if request.method == 'GET':
        return make_response(jsonify({'status': 'ok'}))


@app_views.route('/stats', methods=['GET'])
def stats():
    """ method to response with the count of all objects in storage """
    if request.method == 'GET':
        dct1 = {}
        dct1["amenities"] = storage.count(Amenity)
        dct1["cities"] = storage.count(City)
        dct1["places"] = storage.count(Place)
        dct1["reviews"] = storage.count(Review)
        dct1["states"] = storage.count(State)
        dct1["users"] = storage.count(User)
        return make_response(jsonify(dct1))
