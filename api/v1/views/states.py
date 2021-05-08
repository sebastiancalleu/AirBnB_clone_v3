#!/usr/bin/python3
""" module to create the routes of the blueprint object State """

from api.v1.views import app_views
from flask import jsonify, json, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=["GET", "POST"], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=["GET", "DELETE", "PUT"])
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
            key = "{}.{}".format("State", state_id)
            dct1 = storage.all(State)
            obj1 = None
            for i, j in dct1.items():
                if i == key:
                    obj1 = j.to_dict()
            if obj1 is None:
                abort(404)
            return jsonify(obj1)
    if request.method == "DELETE":
            key = "{}.{}".format("State", state_id)
            dct1 = storage.all(State)
            flag = 0
            for i, j in dct1.items():
                if i == key:
                    storage.delete(j)
                    flag = 1
            if flag == 1:
                return make_response(jsonify({}), 200)
            else:
                abort(404)
    if request.method == "POST":
        try:
            jsondata = request.get_json()
        except:
            abort(400, description="Not a JSON")
        if not jsondata["name"]:
            abort(400, description="Missing name")
        newobj = State(**jsondata)
        newobj.save()
        return make_response(jsonify(newobj.to_dict()), 201)
    if request.method == "PUT":
        try:
            jsonupdt = request.get_json()
        except:
            abort(400, description="Not a JSON")
        key = "{}.{}".format("State", state_id)
        dct1 = storage.all(State)
        obj1 = None
        for i, j in dct1.items():
            if i == key:
                obj1 = j
        if obj1 is None:
            abort(404)
        for i, j in jsonupdt.items():
            setattr(obj1, i, j)
        obj1.save()
        return make_response(jsonify(obj1.to_dict()), 200)
