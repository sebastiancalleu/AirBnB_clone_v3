#!/usr/bin/python3
""" script to create a new app with flask """

from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from models import storage
import os


app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def teardown_db(exception):
    """ method to close the session after each request """
    storage.close()


@app.errorhandler(404)
def resource_not_found(e):
    """ method to handle 404 error """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    if os.getenv("HBNB_API_HOST"):
        hst = os.getenv("HBNB_API_HOST")
    else:
        hst = "0.0.0.0"
    if os.getenv("HBNB_API_PORT"):
        prt = os.getenv("HBNB_API_PORT")
    else:
        prt = 5000
    app.run(host=hst, port=prt, threaded=True)
