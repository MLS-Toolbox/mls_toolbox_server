from mls.model_evaluation import IModelEvaluation

class Evaluate(IModelEvaluation):
    def __init__(self, model, x_test, y_test):
        super.__init__(self)

        self.model = model
        self.x_test = x_test
        self.y_test = y_test
    
    def execute(self):
        model_origin, port = self.model
        model = model_origin.outputs[port]
        x_test_origin, port = self.x_test
        x_test = x_test_origin.outputs[port]
        y_test_origin, port = self.y_test
        y_test = y_test_origin.outputs[port]

        result = model.evaluate(x_test, y_test)

        self.outputs["result"] = result