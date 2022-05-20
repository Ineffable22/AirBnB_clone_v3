#!/usr/bin/python3
"""Create a new view for State objects that handles
all default RESTFul API actions"""
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/amenities', defaults={'amenity_id': None}, methods=['GET'],
                 strict_slashes=False)
@app_views.route('/amenities/<path:amenity_id>')
def get_method(amenity_id):
    if amenity_id is None:
        dict_ = []
        for val in storage.all(Amenity).values():
            dict_.append(val.to_dict())
        return jsonify(dict_)

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<path:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_method(amenity_id):
    if amenity_id is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({})


@app_views.route('/amenity', methods=['POST'],
                 strict_slashes=False)
def post_method():
    res = request.get_json()
    if type(res) != dict:
        return abort(400, {'message': 'Not a JSON'})
    if 'name' not in res:
        return abort(400, {'message': 'Missing name'})
    new_amenity = Amenity(**res)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenity/<path:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_method(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    res = request.get_json()
    if type(res) != dict:
        return abort(400, {'message': 'Not a JSON'})
    for key, value in res.items():
        if key not in ["id", "amenity_id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
