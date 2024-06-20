from mls.data_preprocessing import IDataPreprocessing

class TrainEncoder(IDataPreprocessing):
    def __init__(self, columns, data, encoder):
        super().__init__(self)
        self.columns = columns
        self.data = data
        self.encoder = encoder

    def exec(self):
        data_origin, port = self.data
        dataframe = data_origin.outputs[port]
        data = dataframe.getData()

        encoder_origin, port = self.encoder
        encoder = encoder_origin.outputs[port]

        encoder.fit_transform(data, self.columns)
        dataframe.setData(data)
        self.outputs["encoder"] = encoder

        self.outputs["data"] = dataframe
        