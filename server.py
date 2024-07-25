from flask import Flask, request
import requests
from flask_cors import cross_origin
app = Flask(__name__)
@app.route('/api/create_app', methods=['GET', 'POST'])
@cross_origin()
def request_app():
    # do a request to other flask app
    
    target_url = "http://mls_code_generator:5050/api/create_app"
    response = requests.request(
        method="POST",
        url =target_url,
        json =request.json,
        headers =
            {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
    )
    return response.content

@app.route('/api/test_create_app', methods=['GET', 'POST'])
@cross_origin()
def test_request_app():
    reponse = requests.request(
        method="POST",
        url='http://mls_code_generator:5050',
        headers=
            {
                'Access-Control-Allow-Origin': '*'
            }
        )
    return reponse.text

@app.route('/', methods=['GET', 'POST'])
@cross_origin()
def home():
    return 'hello from mls_toolbox_server'

if __name__ == '__main__':
    from flask_cors import CORS
    CORS(app, supports_credentials=True, origins=['*'])
    app.config["CORS_HEADERS"] = ["Content-Type", "X-Requested-With", "X-CSRFToken"]
    app.run(host= '0.0.0.0', port= 5000, debug=True)