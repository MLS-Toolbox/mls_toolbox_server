""" server.py : Flask server for mls_toolbox. """

import requests
import os

from flask import Flask, request
from flask_cors import cross_origin, CORS
from waitress import serve

app = Flask(__name__)

@app.route('/api/create_app', methods=['GET', 'POST'])
@cross_origin()
def create_app():
    """
    Handles incoming HTTP requests to the '/api/create_app' endpoint.

    Supports both GET and POST methods.

    Makes a POST request to the 'create_app' endpoint
    with the provided JSON data and returns the response content.

    Parameters:
        None

    Returns:
        The content of the response from the target URL.
    """

    target_url = "http://" + os.getenv("MLS_CODE_GENERATOR_URI", "localhost") + ":" + \
        os.getenv("MLS_CODE_GENERATOR_PORT", "5050") + "/api/create_app"
    response = requests.request(
        method="POST",
        url =target_url,
        json =request.json,
        headers =
            {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
        timeout=10
    )
    return response.content

@app.route('/api/test_create_app', methods=['GET', 'POST'])
@cross_origin()
def test_create_app():
    """
    Handles incoming HTTP requests to the '/api/test_create_app' endpoint.

    Supports both GET and POST methods.

    Makes a POST request to the 'test_create_app' endpoint
    with the provided JSON data and returns the response content.

    Parameters:
        None

    Returns:
        The content of the response from the target URL.
    """

    target_url = "http://" + os.getenv("MLS_CODE_GENERATOR_URI", "localhost") + ":" + \
        os.getenv("MLS_CODE_GENERATOR_PORT", "5050")

    reponse = requests.request(
        method = "GET",
        url = target_url,
        headers =
            {
                'Access-Control-Allow-Origin': '*'
            },
        timeout = 10
        )
    return reponse.text

@app.route('/api/rate_app', methods=['GET', 'POST'])
@cross_origin()
def rate_app():
    """
    Handles incoming HTTP requests to the '/api/rate_app' endpoint.

    Supports both GET and POST methods.

    Makes a POST request to the 'rate_app' endpoint
    with the provided JSON data and returns the response content.

    Parameters:
        None

    Returns:
        The content of the response from the target URL.
    """
    target_url = "http://" + os.getenv("MLS_CODE_ASSESS_URI", "localhost") + ":" + \
        os.getenv("MLS_CODE_ASSESS_PORT", "5060") + "/api/test_rate_app"
    response = requests.request(
        method="POST",
        url = target_url,
        json = request.json,
        headers =
            {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
        timeout=100
    )
    return response.content

@app.route('/api/test_rate_app', methods=['GET', 'POST'])
@cross_origin
def test_rate_app():
    """
    Handles incoming HTTP requests to the '/api/test_rate_app' endpoint.

    Supports both GET and POST methods.

    Makes a GET request to the 'test_rate_app' endpoint
    and returns the response content.

    Parameters:
        None

    Returns:
        The content of the response from the target URL.
    """

    target_url = "http://" + os.getenv("MLS_CODE_ASSESS_URI", "localhost") + ":" + \
        os.getenv("MLS_CODE_ASSESS_PORT", "5060")

    response = requests.request(
        method = "GET",
        url = target_url,
        headers =
            {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
        timeout = 10
        )

    return response.text

@app.route('/api/get_config', methods=['GET', 'POST'])
@cross_origin()
def get_config():
    """
    Handles incoming HTTP requests to the '/api/get_config' endpoint.

    Supports both GET and POST methods.

    Makes a GET request to the 'get_config' endpoint
    and returns the response content.

    Parameters:
        None

    Returns:
        The content of the response from the target URL.
    """
    target_url = "http://" + os.getenv("MLS_CODE_GENERATOR_URI", "localhost") + ":" + \
        os.getenv("MLS_CODE_GENERATOR_PORT", "5050") + "/api/get_config"

    response = requests.request(
        method = "GET",
        url = target_url,
        headers =
            {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
        timeout = 10
        )
    return response.content

@app.route('/', methods=['GET', 'POST'])
@cross_origin()
def home():
    """
    Handles incoming HTTP requests to the '/' endpoint.

    Supports both GET and POST methods.

    Returns a simple 'hello' message.
    """
    return 'hello from mls_toolbox_server'

if __name__ == '__main__':
    CORS(app, supports_credentials=True, origins=['*'])
    app.config["CORS_HEADERS"] = ["Content-Type", "X-Requested-With", "X-CSRFToken"]
    
    execution_mode = os.getenv("EXECUTION_MODE", "debug")
    
    HOST = "0.0.0.0"
    PORT = 5000
    
    if execution_mode == "prod":
        serve(app, host = HOST, port = PORT)
    else:
        app.run(host = HOST , port = PORT, debug=True)
