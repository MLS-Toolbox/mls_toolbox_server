from mls.data_cleaning import DataCleaningStep

class ReplaceNull(DataCleaningStep):
    def __init__(self, value, origin):
        super().__init__(
            origin = origin
        )
        
        self.value = value

    def execute(self):
        origin, port = self.origin
        data = origin.get(port).data
        ## FIXME:  data = data.fillna(self.value)
        self.outputs["result"] = data