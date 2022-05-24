#!/usr/bin/python3
"""Create a new view for State objects that handles
all default RESTFul API actions"""
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views as views
from flask import jsonify, abort, request
from .utils import get_resource


@views.route('/amenities', methods=['GET'])
def get_amenities():
    """Get all Amenities"""
    amenities = storage.all("Amenity").values()
    res = [amenity.to_dict() for amenity in amenities]
    return jsonify(res)


@views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """Get Amenity filter by id"""
    amenity = get_resource("Amenity", amenity_id)
    return jsonify(amenity.to_dict())


@views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Delete an Amenity"""
    amenity = get_resource("Amenity", amenity_id)
    amenity.delete()
    storage.save()
    return jsonify({})


@views.route('/amenities', methods=['POST'])
def insert_amenity():
    """Insert new Amenity"""
    body = get_resource(_req=request)
    if 'name' not in body:
        return abort(400, {'message': 'Missing name'})
    new_amenity = Amenity(**body)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Update an Amenity"""
    [amenity, body] = get_resource("Amenity", amenity_id, request)
    for key, value in body.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
