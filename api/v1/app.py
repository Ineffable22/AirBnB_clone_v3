#!/usr/bin/python3
"""
    This script starts a Flask web application
"""
from os import getenv
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from flasgger import Swagger

app = Flask(__name__)

app.url_map.strict_slashes = False

app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})
Swagger(app)


@app.teardown_appcontext
def teardown(self):
    """Removes the current SQLAlchemy Session"""
    return storage.close()


@app.errorhandler(404)
def error(error):
    """
    This function Handles 404 errors
    ---
    parameters:
        name: error
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True, debug=True)
