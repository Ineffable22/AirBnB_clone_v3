#!/usr/bin/python3
"""This module implement a rule that return a view"""
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.place import Place
from .utils import get_resource


@app_views.route("/cities/<city_id>/places", methods=["GET"])
def place_by_city(city_id):
    """View function that return place objects by city"""
    places = get_resource("City", city_id).places
    return jsonify([place.to_dict() for place in places])


@app_views.route("/places/<place_id>", methods=["GET"])
def show_place(place_id):
    """Endpoint that return a Place object"""
    place = get_resource("Place", place_id)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"])
def delete_place(place_id):
    """Endpoint that delete a Place object"""
    place = get_resource("Place", place_id)
    place.delete()
    storage.save()
    return jsonify({})


@app_views.route("/cities/<city_id>/places", methods=["POST"])
def insert_place(city_id):
    """Endpoint that insert a Place object"""
    [_, body] = get_resource("City", city_id, request)
    if not body.get("user_id"):
        abort(400, description="Missing user_id")
    get_resource("User", body.get("user_id"))
    if not body.get("name"):
        abort(400, description="Missing name")
    new_place = Place(**body)
    new_place.city_id = city_id
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places_search", methods=["POST"])
def places_search():
    """Retrieves all Place objects depending of the body of the request"""
    body = get_resource(_req=request)
    keys = ["states", "cities", "amenities"]
    [id_states, id_cities, id_amenities] = [body.get(key, []) for key in keys]
    [places, res] = [[], []]
    sget = storage.get

    if id_states == id_cities == []:
        places = storage.all("Place").values()
    else:
        states = [sget("State", id) for id in id_states if sget("State", id)]
        cities = [city for state in states for city in state.cities]
        cities += [sget("City", id) for id in id_cities if sget("City", id)]
        cities = list(set(cities))
        places = [place for city in cities for place in city.places]

    amenities = [
        sget("Amenity", id) for id in id_amenities if sget("Amenity", id)
    ]

    for place in places:
        res.append(place.to_dict())
        for amenity in amenities:
            if amenity not in place.amenities:
                res.pop()
                break

    return jsonify(res)


@app_views.route("/places/<place_id>", methods=["PUT"])
def update_place(place_id):
    """Endpoint that update a Place object"""
    [place, body] = get_resource("Place", place_id, request)
    for key, value in body.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
