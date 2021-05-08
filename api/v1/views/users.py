#!/usr/bin/python3
""" module to create the routes of the blueprint object City """

from api.v1.views import app_views
from flask import jsonify, json, abort, request, make_response
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET", "POST"],
                 strict_slashes=False)
@app_views.route("/users/<user_id>", methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def usersobj(user_id=None):
    if request.method == "GET":
        if user_id is None:
            dct1 = storage.all(User)
            lt1 = []
            for i, j in dct1.items():
                lt1.append(j.to_dict())
            return jsonify(lt1)
        else:
            obj1 = storage.get(User, user_id)
            if not obj1:
                abort(404)
            return jsonify(obj1.to_dict())
    if request.method == "DELETE":
        obj1 = storage.get(User, user_id)
        if not obj1:
            abort(404)
        storage.delete(obj1)
        return make_response(jsonify({}), 200)
    if request.method == "POST":
        if not request.get_json():
            abort(400, description="Not a JSON")
        jsondata = request.get_json()
        if "email" not in jsondata:
            abort(400, description="Missing email")
        if "password" not in jsondata:
            abort(400, description="Missing password")
        obj1 = User(**jsondata)
        obj1.save()
        return make_response(jsonify(obj1.to_dict()), 201)
    if request.method == "PUT":
        obj1 = storage.get(User, user_id)
        if not obj1:
            abort(404)
        if not request.get_json():
            abort(400, description="Not a JSON")
        jsonupdt = request.get_json()
        for i, j in jsonupdt.items():
            if (i != "id" and i != "created_at" and
                    i != "updated_at" and i != "email"):
                setattr(obj1, i, j)
        obj1.save()
        return make_response(jsonify(obj1.to_dict()), 200)
