#!/user/bin/python3
"""This script starts a Flask web application"""
from os import getenv
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def error(e):
    """Handler for 404 errors"""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown(self):
    """Removes the current SQLAlchemy Session"""
    return storage.close()


if __name__ == '__main__':
    host = getenv("HBNB_API_HOST")
    port = getenv("HBNB_API_PORT")
    app.run(
        host=host if host else "0.0.0.0",
        port=port if port else 5000,
        threaded=True, debug=True
    )
