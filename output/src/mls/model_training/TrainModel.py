from mls.model_training import IModelTraining

class TrainModel(IModelTraining):
    def __init__(self, epochs : int, bach_size : int, features, truth, optimizer, model) -> None:
        super.__init__(self)

        self.epochs = epochs
        self.bach_size = bach_size
        self.features = features
        self.truth = truth
        self.optimizer = optimizer
        self.model = model

    def exec(self):
        model_origin, port = self.model
        model = model_origin.outputs[port]
        optimizer_origin, port = self.optimizer
        optimizer = optimizer_origin.outputs[port]

        features_origin, port = self.features
        features = features_origin.outputs[port]

        truth_origin, port = self.truth
        truth = truth_origin.outputs[port]

        model.fit(features, truth, epochs=self.epochs, batch_size=self.bach_size, optimizer=optimizer)

        self.outputs["model"] = model
