from flask import Flask, request, jsonify
from code_from_config import ModuleHandler, NodesLoader
from flask_cors import cross_origin
import os
import shutil
import json
from fix_editor import fix_editor
import uuid
app = Flask(__name__)

@app.route('/api/create_app', methods=['GET', 'POST'])
@cross_origin()
def add_message():
    content = request.json
    content = fix_editor(content)
    nodes_config_path = 'nodes.json'
    nodes_config = json.load(open(nodes_config_path))
    availableNodes = NodesLoader(content = nodes_config['nodes'])
    # generate random path for this request
    path_head = './'+ str(uuid.uuid4())
    path = path_head + '/src'
    os.mkdir(path_head)
    os.mkdir(path)
    module = ModuleHandler(content = content, nodes = availableNodes.getNodes(), write_path = path)

    module.generateCode()

    # copy mls folder into path
    shutil.copytree('mls', path+'/mls')

    shutil.make_archive(path_head, 'zip', path_head)

    file = open(path_head+'.zip', 'rb')
    data = file.read()
    file.close()
    
    os.remove(path_head+'.zip')
    shutil.rmtree(path_head)

    return data

@app.route('/', methods=['GET', 'POST'])
@cross_origin()
def home():
    return 'hello'

if __name__ == '__main__':
    from flask_cors import CORS
    CORS(app, supports_credentials=True, origins=['*'])
    app.run(host= '0.0.0.0',debug=True)
    app.config["CORS_HEADERS"] = ["Content-Type", "X-Requested-With", "X-CSRFToken"]