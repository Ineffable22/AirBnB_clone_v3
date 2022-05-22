#!/usr/bin/python3
"""module docstring"""
from models import storage
from flask import abort


def get_resource(_cls=None, _id=None, _req=None):
    """Function definition"""
    obj = None
    body = None
    if _cls and _id:
        obj = storage.get(_cls, _id)
        if not obj:
            abort(404)
    if _req:
        try:
            body = _req.get_json()
        except BaseException:
            abort(400, description="Not a JSON")

    if _cls and _id and _req:
        return [obj, body]
    if _cls and _id and not _req:
        return obj
    return body
