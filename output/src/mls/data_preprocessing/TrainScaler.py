from mls.data_preprocessing import IDataPreprocessing

class TrainScaler(IDataPreprocessing):
    def __init__(self, columns, data, scaler):
        super().__init__(self)
        self.columns = columns
        self.data = data
        self.scaler = scaler

    def exec(self):
        data_origin, port = self.data
        dataframe = data_origin.outputs[port]
        data = dataframe.getData()

        scaler_origin, port = self.scaler
        scaler = scaler_origin.outputs[port]

        scaler.fit_transform(data, self.columns)
        dataframe.setData(data)
        self.outputs["scaler"] = scaler

        self.outputs["data"] = dataframe
        