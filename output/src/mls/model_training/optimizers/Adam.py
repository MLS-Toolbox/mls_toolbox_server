from mls.model_training.optimizers import IOptimizer

class Adam(IOptimizer):
    def __init__(self, parameters : str) -> None:
        self.parameters = parameters
        super().__init__()
