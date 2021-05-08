#!/usr/bin/python3
""" module to create the routes of the blueprint object City """

from api.v1.views import app_views
from flask import jsonify, json, abort, request, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET", "POST"])
def statecities(state_id=None):
    """ method for get and post cities """
    if request.method == "GET":
        obj1 = storage.get(State, state_id)
        if not obj1:
            abort(404)
        lt1 = []
        for i in obj1.cities:
            lt1.append(i.to_dict())
        return jsonify(lt1)
    if request.method == "POST":
        objstate = storage.get(State, state_id)
        if not objstate:
            abort(404)
        if not request.get_json():
            abort(400, description="Not a JSON")
        jsondata = request.get_json()
        if "name" not in jsondata:
            abort(400, description="Missing name")
        jsondata["state_id"] = state_id
        objcity = City(**jsondata)
        objcity.save()
        return make_response(jsonify(objcity.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=["GET", "DELETE", "PUT"])
def getcity(city_id=None):
    """ method for get, delete and put cities. """
    if request.method == "GET":
        obj1 = storage.get(City, city_id)
        if not obj1:
            abort(404)
        return jsonify(obj1.to_dict())
    if request.method == "DELETE":
        obj1 = storage.get(City, city_id)
        if not obj1:
            abort(404)
        storage.delete(obj1)
        return make_response(jsonify({}), 200)
    if request.method == "PUT":
        obj1 = storage.get(City, city_id)
        if not obj1:
            abort(404)
        if not request.get_json():
            abort(400, description="Not a JSON")
        jsonupdt = request.get_json()
        for i, j in jsonupdt.items():
            if (i != "id" and i != "created_at" and
                    i != "updated_at" and i != "state_id"):
                setattr(obj1, i, j)
        obj1.save()
        return make_response(jsonify(obj1.to_dict()), 200)
