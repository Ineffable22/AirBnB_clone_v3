#!/user/bin/python3
"""This script starts a Flask web application"""
from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app = blueprint(app_views)

@app.teardown_appcontext()
def teardown():
    return storage.close()


if __name__ == '__main__':
    app.run(host=HBNB_API_HOST ? HBNB_API_HOST : "0.0.0.0",
            port=HBNB_API_PORT ? HBNB_API_PORT : 5000,
            threaded=True)
