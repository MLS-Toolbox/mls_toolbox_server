import json

import yaml
from nodes import DropColumnsNode, EncoderNode, Node, LoadDatasetNode, JoinNode, PredictNode, \
    ReplaceNanNode, MakeCategoricalBinaryNode, ReuseEncoderNode, ReuseScalerNode, ScalerNode, SelectNode, \
    OutputNode, InputNode, EvaluateNode, TrainModelNode, \
    SplitTrainTestNode
    
class Module:
    def __init__(self, id):
        self.id = id
        self.nodes = []
        self.data = ""
        self.name = ""
        self.outs = []

    def addNode(self, node):
        self.nodes.append(node)
    
    def addConnection(self, source, target, sourcePort, targetPort):
        # find target node
        targetNode = None
        for node in self.nodes:
            if node.id == target:
                targetNode = node
                break
        
        # find source node
        sourceNode = None
        for node in self.nodes:
            if node.id == source:
                sourceNode = node
                break
        
        # add dependency
        targetNode.addDependency(targetNode, targetPort, sourceNode, sourcePort)
        sourceNode.addSource(sourcePort, targetNode, targetPort)
    
    def setData(self, data):
        self.data = data
        self.name = data['inputs']['description']['value']

        self.name = self.name.lower()
        self.name = self.name.replace(' ', '_')
    
    def generateCode(self):
        print("Generating code for module: ", self.name)
        code = ""
        copy_nodes = self.nodes.copy()
        while(len(copy_nodes) > 0):
            for node in copy_nodes:
                if not node.isReady():
                    continue
                code += node.generateCode()
                code += "\n"
                copy_nodes.remove(node)
                for p in node.sources:
                    for target, target_port in node.sources[p]:
                        target.pastDependency(target, target_port)
                break
        return code
    
    def getDependenciesCode(self):
        dependencies = dict()
        for node in self.nodes:
            node_dep = node.getDependencies()
            for dep in node_dep.keys():
                if dep not in dependencies:
                    dependencies[dep] = set()
                dependencies[dep].update(node_dep[dep])

        code = ""
        for dep in dependencies.keys():
            code += "from mls." + dep + " import " + ", ".join(dependencies[dep]) + "\n"
        return code

    def getOutput(self, source):
        for node in self.nodes:
            if (type(node) == OutputNode) and (node.getTag() == source):
                    return node.getOutput("")
        return None

    def setInputOrigin(self, target, origin):
        for node in self.nodes:
            if (type(node) == InputNode) and (node.getOutput("value") == target):
                node.setOrigin(origin)
                break
    
    def getDvcConfig(self):
        dvc_config = dict()
        dvc_config['cmd'] = "python3 src/"+self.name+".py"
        dvc_config['deps'] = ["src/"+self.name+".py"]
        dvc_config['outs'] = []
        for node in self.nodes:
            if type(node) == InputNode:
                dvc_config['deps'].append(node.origin.replace("'", ""))
            if type(node) == OutputNode:
                dvc_config['outs'].append(node.getOutput("").replace("'", ""))
            if type(node) == LoadDatasetNode:
                dvc_config['deps'].append("./data/" + node.getPath())
        return dvc_config

def getNodeClass(nodeName: str):
    if nodeName == 'Load dataset':
        return LoadDatasetNode
    elif nodeName == 'Join':
        return JoinNode
    elif nodeName == 'Replace Nan':
        return ReplaceNanNode
    elif nodeName == 'Make Categorical Binary':
        return MakeCategoricalBinaryNode
    elif nodeName == 'Select Columns':
        return SelectNode
    elif nodeName == 'Output':
        return OutputNode
    elif nodeName == 'Input':
        return InputNode
    elif nodeName == 'Evaluate':
        return EvaluateNode
    elif nodeName == 'TrainModelNode':
        return TrainModelNode
    elif nodeName == 'Split train test':
        return SplitTrainTestNode
    elif nodeName == 'Drop Columns':
        return DropColumnsNode
    elif nodeName == 'Reuse Encoder':
        return ReuseEncoderNode
    elif nodeName == 'ReScale Columns':
        return ReuseScalerNode
    elif nodeName == "Encoder":
        return EncoderNode
    elif nodeName == "Scale Columns":
        return ScalerNode
    elif nodeName == "Predict":
        return PredictNode
    else:
        return Node

class ModuleHandler:
    def __init__(self, content):
        self.content = content
        self.all_modules = dict()
        self.all_nodes = dict()

        ## Creating all the modules
        for module in self.content:
            currentModule = Module(module)
            self.all_modules[module] = currentModule
            for node in self.content[module]['nodes']:
                classNode = getNodeClass(node['nodeName'])(node)
                currentModule.addNode(classNode)
                self.all_nodes[classNode.id] = classNode

        ## Adding connections to the modules
        for module in self.all_modules.values():
            module_id = module.id
            for connection in self.content[module_id]['connections']:
                module.addConnection(connection['source'], connection['target'], connection['sourceOutput'], connection['targetInput'])
        
        ## Adding data to the modules from the parent node
        for module in self.all_modules.values():
            if (module.id not in self.all_nodes):
                continue
            module.setData(self.all_nodes[module.id].data)

        ## Inject Outputs into other other module inputs:
        for connection in self.content['root']['connections']:
            source = connection['source']
            target = connection['target']
            sourceOutput = connection['sourceOutput']
            targetInput = connection['targetInput']
            sourceModule = self.all_modules[source]
            targetModule = self.all_modules[target]
            targetModule.setInputOrigin(targetInput, sourceModule.getOutput(sourceOutput))
        
        ## Add parent to each node 
        for module in self.all_modules.values():
            for node in module.nodes:
                node.parent = module

    def generateCode(self):
        root = self.all_modules['root']
        packages = root.nodes
        dvc_config = dict()

        for package in packages:
            c_package = self.all_modules[package.id]
            package_name = c_package.name

            code = c_package.getDependenciesCode()
            code += "\n"
            code += "def main():\n"

            for j in c_package.generateCode().split("\n"):
                code += "\t" + j + "\n"
            
            code += "if __name__ == '__main__':\n"
            code += "\tmain()"

            file_path = "./output/src/" + package_name + ".py"
            file = open(file_path, "w")
            file.write(code)
            file.close()

            dvc_config[package_name] = \
                (c_package.getDvcConfig())
            
            this_package_node = self.all_nodes[package.id]
            modules_id_i_depend_on = set()
            
            for source in this_package_node.dependencies:
                modules_id_i_depend_on.add(source[0].id)

            for module_id in modules_id_i_depend_on:
                package_i_depend_on = self.all_modules[module_id].name
                dvc_config[package_name]['deps'].append("./src/" + package_i_depend_on + ".py")

        yaml.dump({"stages": dvc_config}, open("./output/dvc.yaml", "w"))
            
def main():
    path = 'editor.json'
    content = json.load(open(path))
    moduleArray = ModuleHandler(content['modules'])
    moduleArray.generateCode()
    pass



if __name__ == '__main__':
    main()