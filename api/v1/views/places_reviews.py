#!/usr/bin/python3
""" module to create the routes of the blueprint object City """

from api.v1.views import app_views
from flask import jsonify, json, abort, request, make_response
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=["GET", "POST"],
                 strict_slashes=False)
def placesreviews(place_id=None):
    if request.method == "GET":
        objplace = storage.get(Place, place_id)
        if not objplace:
            abort(404)
        lt1 = []
        for i in objplace.reviews:
            lt1.append(i.to_dict())
        return jsonify(lt1)
    if request.method == "POST":
        objplace = storage.get(Place, place_id)
        if not objplace:
            abort(404)
        if not request.get_json():
            abort(400, description="Not a JSON")
        jsondata = request.get_json()
        if "user_id" not in jsondata:
            abort(400, description="Missing user_id")
        objuser = storage.get(User, jsondata["user_id"])
        if not objuser:
            abort(404)
        if "text" not in jsondata:
            abort(400, description="Missing text")
        jsondata["place_id"] = place_id
        objreview = Review(**jsondata)
        objreview.save()
        return make_response(jsonify(objreview.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=["GET", "DELETE", "PUT"])
def reviews(review_id=None):
    if request.method == "GET":
        objreview = storage.get(Review, review_id)
        if not objreview:
            abort(404)
        return jsonify(objreview.to_dict())
    if request.method == "DELETE":
        objreview = storage.get(Review, review_id)
        if not objreview:
            abort(404)
        storage.delete(objreview)
        return make_response(jsonify({}), 200)
    if request.method == "PUT":
        objreview = storage.get(Review, review_id)
        if not objreview:
            abort(404)
        if not request.get_json():
            abort(400, description="Not a JSON")
        jsonupdt = request.get_json()
        for i, j in jsonupdt.items():
            if (i != "id" and i != "user_id" and
                    i != "place_id" and i != "created_at" and
                    i != "updated_at"):
                setattr(objreview, i, j)
        objreview.save()
        return make_response(jsonify(objreview.to_dict()), 200)
