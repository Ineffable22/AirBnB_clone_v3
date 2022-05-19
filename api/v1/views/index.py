import json
from api.v1.views import app_views


@app_views.route("/status")
def index():
    """View funcion that return a json message"""
    return json.loads({"status": "OK"})
