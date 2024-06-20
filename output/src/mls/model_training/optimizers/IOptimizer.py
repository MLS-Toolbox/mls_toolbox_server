from mls.model_training import IModelTraining

class IOptimizer(IModelTraining):
    def __init__(self) -> None:
        super().__init__()