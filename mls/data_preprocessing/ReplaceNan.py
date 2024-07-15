from mls.data_preprocessing import DataPreProcessingStep

class ReplaceNan(DataPreProcessingStep):
    def __init__(self, value, origin):
        self.value = value
        self.origin = origin

    def execute(self):
        origin, port = self.origin
        data = origin.get(port).data
        data = data.fillna(self.value)
        self.outputs["result"] = data
