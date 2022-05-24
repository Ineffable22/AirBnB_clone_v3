#!/usr/bin/python3
"""New view for the link between Place objects and Amenity objects"""
from api.v1.views import app_views as views
from models import storage
from os import getenv
from flask import jsonify, abort
from .utils import get_resource

mode = getenv("HBNB_TYPE_STORAGE")


@views.route("/places/<place_id>/amenities", methods=["GET"])
def get_amenities(place_id):
    """Get all amenities of a place object"""
    place = get_resource("Place", place_id)
    if mode == "db":
        amenities = place.amenities
        response = [amenity.to_dict() for amenity in amenities]
    else:
        ids = place.amenity_ids
        response = [storage.get("Amenity", id).to_dict() for id in ids]
    return jsonify(response)


@views.route("/places/<place_id>/amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity(place_id, amenity_id):
    """Delete a Amenity object by its id from a Place object"""
    place = get_resource("Place", place_id)
    amenity = get_resource("Amenity", amenity_id)
    if mode == "db":
        if amenity not in place.amenities:
            abort(404)
    else:
        if amenity.id not in place.amenity_id:
            abort(404)
    amenity.delete()
    storage.save()
    return jsonify({})


@views.route("places/<place_id>/amenities/<amenity_id>", methods=["POST"])
def insert_amenity_in_place(place_id, amenity_id):
    """Insert new amenity object into Place object"""
    place = get_resource("Place", place_id)
    amenity = get_resource("Amenity", amenity_id)
    if mode == "db":
        if amenity in place.amenities:
            return jsonify(amenity.to_dict())
        else:
            place.amenities.append(amenity)
    else:
        if amenity.id in place.amenity_id:
            return jsonify(amenity.to_dict())
        else:
            place.amenity_id.append(amenity.id)
    storage.save()
    return jsonify(amenity.to_dict()), 201
