from flask import Flask, request, jsonify
from code_from_config import ModuleHandler, NodesLoader
from flask_cors import cross_origin
import os
import shutil
import json

app = Flask(__name__)

@app.route('/api/create_app', methods=['GET', 'POST'])
@cross_origin()
def add_message():
    content = request.json
    nodes_config_path = 'nodes.json'
    nodes_config = json.load(open(nodes_config_path))
    availableNodes = NodesLoader(content = nodes_config['nodes'])
    module = ModuleHandler(content = content, nodes = availableNodes.getNodes())
    
    # remove files from previous run

    folder = './output/src'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    if os.path.exists('./output/dvc.yaml'):
        os.unlink('./output/dvc.yaml')

    module.generateCode()

    shutil.make_archive('./output', 'zip', './output')

    folder = './output/src'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    os.unlink('./output/dvc.yaml')
    

    file = open('./output.zip', 'rb')
    data = file.read()
    file.close()
    return data

if __name__ == '__main__':
    from flask_cors import CORS
    CORS(app, supports_credentials=True, origins=['http://localhost:8000'])
    app.run(host= '0.0.0.0',debug=True)
    app.config["CORS_HEADERS"] = ["Content-Type", "X-Requested-With", "X-CSRFToken"]