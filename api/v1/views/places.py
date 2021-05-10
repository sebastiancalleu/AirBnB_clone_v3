#!/usr/bin/python3
""" module to create the routes of the blueprint object City """

from api.v1.views import app_views
from flask import jsonify, json, abort, request, make_response
from models import storage
from models.place import Place
from models.city import City
from models.user import User

@app_views.route("/cities/<city_id>/places", methods=["GET", "POST"],
                 strict_slashes=False)
def placesincity(city_id=None):
    if request.method == "GET":
        objcity = storage.get(City, city_id)
        if not objcity:
            abort(404)
        lt1 = []
        for i in objcity.places:
            lt1.append(i.to_dict())
        return jsonify(lt1)
    if request.method == "POST":
        objcity = storage.get(City, city_id)
        if not objcity:
            abort(404)
        if not request.get_json():
            abort(400, description="Not a JSON")
        jsondata = request.get_json()
        if "user_id" not in jsondata:
            abort(400, description="Missing user_id")
        objuser = storage.get(User, jsondata["user_id"])
        if not objuser:
            abort(404)
        if "name" not in jsondata:
            abort(400, description="Missing name")
        jsondata["city_id"] = city_id
        objplace = Place(**jsondata)
        objplace.save()
        return make_response(jsonify(objplace.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def placeobj(place_id=None):
    if request.method == "GET":
        objplace = storage.get(Place, place_id)
        if not objplace:
            abort(404)
        return jsonify(objplace.to_dict())
    if request.method == "DELETE":
        objplace = storage.get(Place, place_id)
        if not objplace:
            abort(404)
        storage.delete(objplace)
        return make_response(jsonify({}), 200)
    if request.method == "PUT":
        objplace = storage.get(Place, place_id)
        if not objplace:
            abort(404)
        if not request.get_json():
            abort(400, description="Not a JSON")
        jsonupdt = request.get_json()
        for i, j in jsonupdt.items():
            if (i != "id" and i != "city_id" and
                    i != "created_at" and i != "updated_at"):
                setattr(objplace, i, j)
        objplace.save()
        return make_response(jsonify(objplace.to_dict()), 200)
