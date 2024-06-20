from sklearn.linear_model import LinearRegression
from mls.model_training.models import IModelStep

class LinarRegression(IModelStep):
    def __init__(self, parameters : str) -> None:
        self.parameters = parameters
        super.__init__(self)

    def execute(self):
        self.outputs["model"] = LinearRegression()