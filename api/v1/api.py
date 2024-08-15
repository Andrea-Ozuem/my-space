#!/usr/bin/python3
""" Flask Application """
from models import storage
from api.v1.views import app_views, auth_views
from os import environ
from flask import Flask, render_template, make_response, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pytz
from models.user import User

load_dotenv()
app = Flask(__name__)

app.register_blueprint(app_views)
app.register_blueprint(auth_views)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """ 404 Error"""
    return make_response(jsonify({'error': error.description}), 404)

@app.errorhandler(401)
def not_found(error):
    """ 401 Error"""
    return make_response(jsonify({'error': error.description }), 401)

@app.errorhandler(400)
def not_found(error):
    """ 400 Error"""
    return make_response(jsonify({'error': error.description }), 400)

if __name__ == "__main__":
    """ Main Function """
    host = environ.get('API_HOST')
    port = environ.get('API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5001'
    app.run(host=host, port=port, threaded=True)
