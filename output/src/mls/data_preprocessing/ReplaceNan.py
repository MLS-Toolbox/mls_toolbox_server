from mls.data_preprocessing import IDataPreprocessing

class ReplaceNan(IDataPreprocessing):
    def __init__(self, value, origin):
        self.value = value
        self.origin = origin

    def execute(self):
        origin, port = self.origin
        data = origin.outputs[port].data
        data = data.fillna(self.value)
        self.outputs["result"] = data
