from mls.data_transformation import IDataTransformation

class DropColumns(IDataTransformation):
    def __init__(self, columns, origin):
        super().__init__(self)
        self.columns = columns
        self.origin = origin

    def exec(self):
        origin, port = self.origin
        dataframe = origin.outputs[port]
        data = dataframe.getData()
        data = data.drop(self.columns, axis=1)
        dataframe.setData(data)
        self.outputs["resulting_table"] = dataframe