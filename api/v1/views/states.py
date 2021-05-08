#!/usr/bin/python3
""" module to create the routes of the blueprint object State """

from api.v1.views import app_views
from flask import jsonify, json, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=["GET", "POST"], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def states(state_id=None):
    """ method to manipulate states object """
    if request.method == "GET":
        if state_id is None:
            dct1 = storage.all(State)
            lt1 = []
            for i in dct1.values():
                lt1.append(i.to_dict())
            return jsonify(lt1)
        else:
            obj1 = storage.get(State, state_id)
            if not obj1:
                abort(404)
            return jsonify(obj1.to_dict())
    if request.method == "DELETE":
            obj1 = storage.get(State, state_id)
            if not obj1:
                abort(404)
            storage.delete(obj1)
            return make_response(jsonify({}), 200)
    if request.method == "POST":
        if not request.get_json():
            abort(400, description="Not a JSON")
        jsondata = request.get_json()
        if "name" not in jsondata:
            abort(400, description="Missing name")
        newobj = State(**jsondata)
        newobj.save()
        return make_response(jsonify(newobj.to_dict()), 201)
    if request.method == "PUT":
        obj1 = storage.get(State, state_id)
        if not obj1:
            abort(404)
        if not request.get_json():
            abort(400, description="Not a JSON")
        jsonupdt = request.get_json()
        for i, j in jsonupdt.items():
            if i != "id" and i != "created_at" and i != "updated_at":
                setattr(obj1, i, j)
        obj1.save()
        return make_response(jsonify(obj1.to_dict()), 200)
