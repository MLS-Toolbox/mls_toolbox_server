class Node:
    def __init__(self, data):
        self.id = data['id']
        self.data = data['data']
        self.dependencies = []
        self.sources = dict()
        self.nodeName = data['nodeName']
        self.parent = None
        self.ready = []

    def addDependency(self, dep, port, src, srcPort):
        self.dependencies.append((src, srcPort, dep, port))
        self.ready.append(False)
    
    def addSource(self, my_port, target, target_port):
        if my_port in self.sources:
            self.sources[my_port].append((target, target_port))
        else:
            self.sources[my_port] = [(target, target_port)]
    
    def isReady(self):
        for i in self.ready:
            if not i: return False
        return True
    
    def pastDependency(self,src, srcPort):
        for i, dep in enumerate(self.dependencies):
            if dep[2] == src and dep[3] == srcPort:
                self.ready[i] = True
                return None
            
    def _getInput(self, side):
        for dep in self.dependencies:
            if dep[3] == side:
                return dep[0], dep[1]
        return None
            
    def getOutput(self, port):
        return port

    def __repr__(self) -> str:
        return self.nodeName

    def __str__(self) -> str:
        return self.nodeName
    
    def generateCode(self):
        return "# " + self.nodeName + " not implemented yet\n"
    
    def portIsMultiple(self, port):
        if port in self.sources:
            return len(self.sources[port]) > 1
        
    def isOutputMultiple(self, port):
        for dep in self.dependencies:
            if dep[3] == port:
                return dep[0].portIsMultiple(dep[1])
        return None
    
    def getDependencies(self) -> dict:
        return dict()

    def getParameter(self, nodeID):
        if self.parent is None:
            return "'NONE'"
        parameterNode = self.parent.getNode(nodeID)
        if parameterNode is None:
            return "'NONE'"

        return parameterNode.getParameter()

class LoadDatasetConfig:
    def __init__(self, data):
        self.path = data['inputs']['path']['value'].lower()
        self.tag = self.path.split(".")[0]
        self.loader = self.getLoader(self.path)

    def getLoader(self, path):
        if path.endswith('.csv'):
            return 'CSVLoader'
        elif path.endswith('.json'):
            return 'JSONLoader'
        elif path.endswith('.parquet'):
            return 'ParquetLoader'
        else:
            return 'UnknownLoader'

class LoadDatasetNode(Node):
    def __init__(self, data):
        super().__init__(data)
        self.config = LoadDatasetConfig(data["data"])
    def getLoader(self):
        return self.config.loader

    def getTag(self):
        return self.config.tag
    
    def getPath(self):
        return self.config.path
    
    def getOutput(self, port):
        return self.getTag()
    
    def generateCode(self):
        code = self.getTag() + " = "
        code += "Dataset(\n\tloader = " + self.getLoader() + ",\n"
        code += "\tpath = './data/" + self.getPath() + "'\n"
        code += ")\n"
        return code
    
    def getDependencies(self) -> dict:
        return {
            'loaders': {self.getLoader()},
            'data_manager': {'Dataset'}
        }

class JoinConfig:
    def __init__(self, data) -> None:
        self.join_type = data['inputs']['type']['value']

class JoinNode(Node): # Done
    def __init__(self, data):
        super().__init__(data)
        self.config = JoinConfig(data["data"])

    def getLeftInput(self):
        left_dependency, port = self._getInput('left_table')
        return left_dependency.getOutput(port)
    
    def getRightInput(self):
        right_dependency, port = self._getInput('right_table')
        return right_dependency.getOutput(port)
    
    def getJoinType(self):
        return self.config.join_type

    def getIndex(self):
        return "not implemented yet"

    def getTag(self):
        return self.getLeftInput()

    def getOutput(self, port):
        return self.getTag()
    
    def generateCode(self):
        code = self.getLeftInput()
        code += ".join_data(\n"
        code += "\tright = " + self.getRightInput() + ",\n"
        code += "\tindex = '" + self.getIndex() + "',\n"
        code += "\thow = '" + self.getJoinType() + "'\n"
        code += ")\n"
        return code
    
    def getDependencies(self) -> dict:
        return {
        }

class ReplaceNanConfig:
    def __init__(self, data):
        self.value = data['inputs']['value']['value']

class ReplaceNanNode(Node): # Done
    def __init__(self, data):
        super().__init__(data)
        self.config = ReplaceNanConfig(data['data'])

    def _getInput(self):
        dep = self.dependencies[0]
        return dep[0], dep[1]
    
    def getTag(self):
        dep, port = self._getInput()
        return dep.getOutput(port)
    
    def getValue(self):
        return self.config.value
    
    def getOutput(self, port):
        return self.getTag()
    
    def generateCode(self):
        code = self.getTag()
        code += ".replace_nans(\n"
        code += "\tvalue = " + self.getValue() + "\n"
        code += ")\n"
        return code
    
    def getDependencies(self) -> dict:
        return {
        }

class MakeCategoricalBinaryConfig:
    def __init__(self, data):
        self.columns = data['inputs']['columns']['value'].split(' ')
        self.tag = data['inputs']['description']['value']

class MakeCategoricalBinaryNode(Node):
    def __init__(self, data):
        super().__init__(data)
        self.config = MakeCategoricalBinaryConfig(data['data'])

    def _getInput(self):
        dep = self.dependencies[0]
        return dep[0], dep[1]
    
    def getOrigin(self):
        dep, port = self._getInput()
        return dep.getOutput(port)
    
    def getTag(self):
        return self.config.tag
    
    def getColumns(self):
        return self.config.columns
    
    def getOutput(self, port):
        return self.getOrigin()
    
    def generateCode(self):
        code = self.getOrigin()
        code += ".make_categorical_binary(\n"
        code += "\tcolumns = " + str(self.getColumns()) + "\n"
        code += ")\n"
        return code
    
    def getDependencies(self) -> dict:
        return {
        }

class SelectConfig:
    def __init__(self, data):
        self.columns = data['inputs']['columns']['value'].split(' ')
        self.description = data['inputs']['description']['value']

class SelectNode(Node):  # DONE
    def __init__(self, data):
        super().__init__(data)
        self.config = SelectConfig(data['data'])

    def _getInput(self):
        dep = self.dependencies[0]
        return dep[0], dep[1]
    
    def getOrigin(self):
        dep, port = self._getInput()
        return dep.getOutput(port)
    
    def getTag(self):
        return self.getOrigin()
    
    def getColumns(self):
        return self.config.columns

    def getOutput(self, port):
        if self.isOutputMultiple("origin_table"):
            return self.config.description.replace(" ", "_").lower() + "_" + self.getOrigin()
        return self.getOrigin()
    
    def generateCode(self):
        code = ""
        if self.isOutputMultiple("origin_table"):
            code += self.getOutput("origin_table") + " = " + self.getOrigin() + ".copy()\n"
        code += self.getOutput("origin_table")
        code += ".select_data(\n"
        code += "\tcolumns = " + str(self.getColumns()) + "\n"
        code += ")\n"
        return code
    
    def getDependencies(self) -> dict:
        return {}

class DropColumnsConfig:
    def __init__(self, data):
        self.columns = data['inputs']['columns']['value'].split(' ')
        self.description = data['inputs']['description']['value']

class DropColumnsNode(Node): # DONE
    def __init__(self, data):
        super().__init__(data)
        self.config = DropColumnsConfig(data['data'])

    def _getInput(self):
        dep = self.dependencies[0]
        return dep[0], dep[1]
    
    def getOrigin(self):
        dep, port = self._getInput()
        return dep.getOutput(port)
    
    def getTag(self):
        return self.getOrigin()
    
    def getColumns(self):
        return self.config.columns
        
    def getOutput(self, port):
        if self.isOutputMultiple("origin_table"):
            return self.config.description.replace(" ", "_").lower() + "_" + self.getOrigin()
        return self.getOrigin()
    
    def generateCode(self):
        code = ""
        if self.isOutputMultiple("origin_table"):
            code += self.getOutput("origin_table") + " = " + self.getOrigin() + ".copy()\n"
        code += self.getOutput("origin_table")
        code += ".drop_columns(\n"
        code += "\tcolumns = " + str(self.getColumns()) + "\n"
        code += ")\n"
        return code
    
    def getDependencies(self) -> dict:
        return {}

class OutputConfig:
    def __init__(self, data):
        self.key = data['inputs']['key']['value']

class OutputNode(Node): # DONE
    def __init__(self, data):
        super().__init__(data)
        self.config = OutputConfig(data['data'])

    def _getInput(self):
        dep = self.dependencies[0]
        return dep[0], dep[1]
    
    def getOrigin(self):
        dep, port = self._getInput()
        return dep.getOutput(port)
    
    def getOutput(self, port):
        return "'./outputs/" + self.config.key +  "'"
    
    def getTag(self):
        return self.data['inputs']['key']['value']
    
    def generateCode(self):
        code = ""
        code += "StepManager.save(\n"
        code += "\torigin = " + self.getOrigin() + ",\n"
        code += "\tpath = './outputs/" + self.config.key + "'\n"
        code += ")\n"
        return code
    
    def getDependencies(self) -> dict:
        return {
            'step_manager': {'StepManager'}
        }

class InputConfig:
    def __init__(self, data):
        self.key = data['inputs']['key']['value']

class InputNode(Node): # DONE
    def __init__(self, data):
        super().__init__(data)
        self.config = InputConfig(data['data'])
        self.origin = ""

    def setOrigin(self, origin):
        self.origin = origin

    def getOutput(self, port):
        return self.config.key
    
    def generateCode(self):
        code = self.data['inputs']['key']['value'] + " = "
        code += "StepManager.load(\n"
        code += "\tpath = " + self.origin + "\n"
        code += ")\n"
        return code
    
    def getDependencies(self) -> dict:
        return {
            'step_manager': {'StepManager'}
        }

class EvaluateNode(Node): # DONE
    def _getInput(self, side):
        for dep in self.dependencies:
            if dep[3] == side:
                return dep[0], dep[1]
        return None
    def getModel(self):
        dep, port = self._getInput('model')
        return dep.getOutput(port)
    def getLabels(self):
        dep, port = self._getInput('label')
        return dep.getOutput(port)
    def getTruth(self):
        dep, port = self._getInput('truth')
        return dep.getOutput(port)
    
    def generateCode(self):
        code = self.getModel() + ".evaluate(\n"
        code += "\tfeatures = " + self.getLabels() + ",\n"
        code += "\ttruth = " + self.getTruth() + "\n"
        code += ")\n"
        return code

    def getDependencies(self) -> dict:
        return {}

class TrainModelConfig:
    def __init__(self, data):
        self.model = data['inputs']['type']['value']['value'].replace(" ", "")
        self.parameters = data['inputs']['parameters']['value'].split(',')
        self.model_tag = data['inputs']['model_tag']['value']

class TrainModelNode(Node): # Done
    def __init__(self, data):
        super().__init__(data)
        self.config = TrainModelConfig(data['data'])

    def _getInput(self, side):
        for dep in self.dependencies:
            if dep[3] == side:
                return dep[0], dep[1]
        return None
    
    def getModel(self):
        model_name = self.config.model
        parameters = self.config.parameters
        txt = model_name + "(\n"
        for parameter in parameters[:-1]:
            txt += "\t\t" + parameter + ",\n"
        if (len(parameters) > 0):
            txt += "\t\t" + parameters[-1] + "\n"
        txt += "\t)"
        return txt
    
    def getLabels(self):
        dep, port = self._getInput('labels')
        return dep.getOutput(port)
    
    def getFeatures(self):
        dep, port = self._getInput('truth')
        return dep.getOutput(port)
    
    def getOutput(self, port):
        return self.config.model_tag
    
    def generateCode(self):
        code = self.getOutput("") + " = Model(\n"
        code += "\tmodel = " + self.getModel() + ",\n"
        code += "\tfeatures = " + self.getLabels() + ",\n"
        code += "\ttruth = " + self.getFeatures() + "\n"
        code += ")\n"
        return code
    
    def getDependencies(self) -> dict:
        return {
            'models': {self.config.model},
            'model_manager': {'Model'}
        }

class SplitTrainTestConfig: 
    def __init__(self, data, parent : Node):
        if data['inputs']['train_percentage']['isParam']:
            parent.getParameter(data['inputs']['train_percentage']['paramRef'])
            self.train_percentage = data['inputs']['train_percentage']['paramRef']
        else:
            self.train_percentage = data['inputs']['train_percentage']['value']

class SplitTrainTestNode(Node): # DONE
    def __init__(self, data):
        super().__init__(data)
        self.config = SplitTrainTestConfig(data['data'], self)

    def _getInput(self, side):
        for dep in self.dependencies:
            if dep[3] == side:
                return dep[0], dep[1]
        return None
    
    def getSource(self):
        res = self._getInput('features')
        if res == None:
            return "NONE"
        dep, port = res

        return dep.getOutput(port)

    def getTags(self):
        res = self._getInput('truth')
        if res == None:
            return "NONE"
        dep, port = res
        return dep.getOutput(port)
    
    def getOutput(self, port):
        return port
    
    def generateCode(self):
        code = "features_train, features_test, truth_train, truth_test" +  "= split_train_test(\n"
        code += "\tfeatures = " + self.getSource() + ",\n"
        code += "\ttruth = " + self.getTags() + ",\n"
        code += "\tpercentage = " + str(self.config.train_percentage) + "\n"
        code += ")\n"
        return code
    
    def getDependencies(self) -> dict:
        return {
            'data_manager': {'split_train_test'}
        }
    
class ReuseEncoderNode(Node): # DONE
    def __init__(self, data):
        super().__init__(data)

    def _getInput(self, side):
        for dep in self.dependencies:
            if dep[3] == side:
                return dep[0], dep[1]
        return None
    
    def getEncoder(self):
        return self._getInput("encoder")[0].getOutput("")

    def getOutput(self, port):
        return self._getInput("input_dataset")[0].getOutput(port)
    
    def generateCode(self):
        txt = self.getEncoder() + ".transform(\n"
        txt += "\tdata = " + self.getOutput("") + "\n"
        txt += ")\n"
        return txt

class ReuseScalerNode(Node): # DONE
    def __init__(self, data):
        super().__init__(data)

    def _getInput(self, side):
        for dep in self.dependencies:
            if dep[3] == side:
                return dep[0], dep[1]
        return None
    
    def getScaler(self):
        return self._getInput("scaler")[0].getOutput("")

    def getOutput(self, port):
        return self._getInput("input_dataset")[0].getOutput(port)
    
    def generateCode(self):
        txt = self.getScaler() + ".transform(\n"
        txt += "\tdata = " + self.getOutput("") + "\n"
        txt += ")\n"
        return txt

class EncoderConfig:
    def __init__(self, data):
        self.encoder = data['inputs']['type']['value'].replace(" ", "")
        self.parameters = data['inputs']['parameters']['value'].split(',')
        self.columns = data['inputs']['columns']['value'].split(' ')

class EncoderNode(Node): # DONE
    def __init__(self, data):
        super().__init__(data)
        self.config = EncoderConfig(data['data'])
    
    def getData(self):
        dep, port = self._getInput('input_dataset')
        return dep.getOutput(port)
    
    def getOutput(self, port):
        if port == 'encoder':
            return port
        else:
            return self.getData()
    
    def generateCode(self):
        code = self.getOutput("encoder") + " = Encoder(\n"
        code += "\tencoder = " + self.config.encoder + "(\n"
        code += "\t\tcols = " + str(self.config.columns) + ",\n"
        for i in self.config.parameters[:-1]:
            code += "\t\t" + i + ",\n"
        code += "\t\t" + self.config.parameters[-1] + "\n"
        code += "\t),\n"
        code += ")\n"

        code += self.getOutput("encoder") + ".fit_transform(\n"
        code += "\tdata = " + self.getData() + "\n"
        code += ")\n"

        return code
    
    def getDependencies(self) -> dict:
        return {
            'encoders': {self.config.encoder},
            'preprocessing_manager': {'Encoder'}
        }

class ScalerConfig:
    def __init__(self, data):
        self.scaler = data['inputs']['type']['value'].replace(" ", "")
        #self.parameters = data['inputs']['parameters']['value'].split(',')
        self.columns = data['inputs']['columns']['value'].split(' ')

class ScalerNode(Node): # done
    def __init__(self, data):
        super().__init__(data)
        self.config = ScalerConfig(data['data'])
    
    def getData(self):
        dep, port = self._getInput('input_dataset')
        return dep.getOutput(port)
    
    def getOutput(self, port):
        if port == 'scaler':
            return port
        else:
            return self.getData()
    
    def generateCode(self):
        code = self.getOutput("scaler") + " = Scaler(\n"
        code += "\tscaler = " + self.config.scaler + "(),\n" # FIXME: Add parameters
        code += "\t\tcolumns= " + str(self.config.columns) + "\n"
        code += ")\n"

        code += self.getOutput("scaler") + ".fit_transform(\n"
        code += "\tdata = " + self.getData() + "\n"
        code += ")\n"

        return code
    
    def getDependencies(self) -> dict:
        return {
            'scalers': {self.config.scaler},
            'preprocessing_manager': {'Scaler'}
        }


class PredictNode(Node): # DONE
    def __init__(self, data):
        super().__init__(data)
        self.data = data['data']
    
    def generateCode(self):
        code = self._getInput("model")[0].getOutput("") + ".predict(\n"
        code += "\tdata = " + self._getInput("features")[0].getOutput("") + ",\n"
        code += "\tpath = './outputs/" + self.data['inputs']['path']['value'] + "'\n"
        code += ")\n"
        return code

    def getDependencies(self) -> dict:
        return {}
    
class ParamNode(Node): # Done
    def __init__(self, data):
        super().__init__(data)
        self.data = data['data']
    
    def generateCode(self):
        return ""
    
    def getParameter(self):
        description = self.data['inputs']['key']['des'].replace(" ", "_").replace("\n", "").lower()
        code = "ParameterManager.get(" + description + ")"
        return code
    
    def getDependencies(self) -> dict:
        return {
            "step_manager": {"ParameterManager"}
        }