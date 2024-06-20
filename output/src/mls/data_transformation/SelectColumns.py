from mls.data_transformation import IDataTransformation

class SelectColumns(IDataTransformation):
    def __init__(self, columns, origin):
        super().__init__(self)
        self.columns = columns
        self.origin = origin

    def exec(self):
        origin, port = self.origin
        dataframe = origin.outputs[port]
        data = dataframe.getData()

        data = data[self.columns]
        dataframe.setData(data)
        self.outputs["resulting_table"] = dataframe
