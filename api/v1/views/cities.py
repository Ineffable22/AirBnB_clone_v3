#!/usr/bin/python3
"""This module implement a rule that return a view"""
from json.decoder import JSONDecodeError
from flask import jsonify, abort, request
import models
import json
from api.v1.views import app_views
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", methods=["GET"])
def cities_by_state(state_id):
    """View function that return object by state"""
    state = models.storage.all(State).get("State.{}".format(state_id))
    if state is None:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route("/cities/<city_id>", methods=["GET"])
def show_city(city_id):
    """Endpoint that return a City object"""
    city = models.storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    """Endpoint that delete a City object"""
    city = models.storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    models.storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def insert_city(state_id):
    """Endpoint that insert a City object"""
    state = models.storage.get(State, state_id)
    if state is None:
        abort(404)
    props = request.get_json()
    try:
        json.dumps(props)
    except JSONDecodeError:
        abort(404, description="Not a JSON")
    if not props.get("name"):
        abort(400, description="Missing name")
    props.update({"state_id": state_id})
    new_city = City(**props)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"])
def update_city(city_id):
    """Endpoint that update a City object"""
    city = models.storage.get(City, city_id)
    if city is None:
        abort(404)
    props = request.get_json()
    try:
        json.dumps(props)
    except JSONDecodeError:
        abort(400, description="Not a JSON")
    for key, value in props.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, value)
    models.storage.save()
    return jsonify(city.to_dict()), 200
