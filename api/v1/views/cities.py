#!/usr/bin/python3
"""This module implement a rule that return a view"""
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views as views
from models.city import City
from .utils import get_resource


@views.route("/states/<state_id>/cities", methods=["GET"])
def get_cities(state_id):
    """View function that return city objects by state"""
    state = get_resource("State", state_id)
    return jsonify([city.to_dict() for city in state.cities])


@views.route("/cities/<city_id>", methods=["GET"])
def get_city(city_id):
    """Endpoint that return a City object"""
    city = get_resource("City", city_id)
    return jsonify(city.to_dict())


@views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    """Endpoint that delete a City object"""
    city = get_resource("City", city_id)
    city.delete()
    storage.save()
    return jsonify({})


@views.route("/states/<state_id>/cities", methods=["POST"])
def insert_city(state_id):
    """Endpoint that insert a City object"""
    [_, body] = get_resource("State", state_id, request)
    if not body.get("name"):
        abort(400, description="Missing name")
    new_city = City(**body)
    new_city.state_id = state_id
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@views.route("/cities/<city_id>", methods=["PUT"])
def update_city(city_id):
    """Endpoint that update a City object"""
    [city, body] = get_resource("City", city_id, request)
    for key, value in body.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
