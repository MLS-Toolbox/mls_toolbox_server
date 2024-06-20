from mls.data_acquisition import IDataAcquisition
from mls.data_acquisition import DataFrame
from mls.loaders import *

class LoadDataset(IDataAcquisition):
    def __init__(self, path : str, loader : str):
        super().__init__(),
        termination = path.split(".")[-1]
        self.loader = self.getLoaderFromTermination(termination)
        self.path = path
    def execute(self):
        data = DataFrame(
            loader = self.loader,
            path = self.path 
        )

        self.outputs["resulting_table"] = data

    def getLoaderFromTermination(self, termination : str):
        if termination == "csv":
            return CSVLoader
