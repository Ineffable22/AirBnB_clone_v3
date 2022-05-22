#!/usr/bin/python3
"""This module implement a rule that return a view"""
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User
from models.state import State


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def place_by_city(city_id):
    """View function that return place objects by city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route("/places/<place_id>", methods=["GET"],
                 strict_slashes=False)
def show_place(place_id):
    """Endpoint that return a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """Endpoint that delete a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def insert_place(city_id):
    """Endpoint that insert a Place object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    res = request.get_json()
    if type(res) != dict:
        abort(400, description="Not a JSON")
    if not res.get("user_id"):
        abort(400, description="Missing user_id")
    user = storage.get(User, res.get("user_id"))
    if user is None:
        abort(404)
    if not res.get("name"):
        abort(400, description="Missing name")
    new_place = Place(**res)
    new_place.city_id = city_id
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/api/v1/places_search", methods=["POST"],
                 strict_slashes=False)
def places_search():
    """Retrieves all Place objects depending of the body of the request"""
    print("volvimos peraaa")
    body = request.get_json()
    id_states = body.get("states") if body.get("states") else []
    id_cities = body.get("cities") if body.get("cities") else []
    id_amenities = body.get("amenities") if body.get("amenities") else []
    places = []
    if type(body) != dict:
        abort(400, description="Not a JSON")
    if body == {} or len(id_states + id_cities + id_amenities) == 0:
        places = storage.all(Place).values()
    elif id_states != [] and id_cities != []:
        states = [storage.get(State, _id) for _id in id_states]
        cities = [city for state in states for city in state.cities]
        cities += [storage.get(City, _id) for _id in id_cities]
        cities = list(set(cities))
        places = [place for city in cities for place in city.places]
    elif id_states != [] and id_cities == []:
        states = [storage.get(State, _id) for _id in id_states]
        cities = [city for state in states for city in state.cities]
        places = [place for city in cities for place in city.places]
        # places = [place for _id in id_states for city in storage.get(State, _id).cities for place in city.places]
    elif id_cities != []:
        cities = [storage.get(City, _id) for _id in id_cities]
        places = [place for city in cities for place in city.places]
    if id_amenities != []:
        places = list(filter(lambda e: e.amenities in id_amenities, places))
    return jsonify([place.to_dict() for place in places])


@app_views.route("/places/<place_id>", methods=["PUT"],
                 strict_slashes=False)
def update_place(place_id):
    """Endpoint that update a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    res = request.get_json()
    if type(res) != dict:
        abort(400, description="Not a JSON")
    for key, value in res.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
