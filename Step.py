
class Step:
    def __init__(self):
        self.inputs = dict()
        self.outputs = dict()
    def execute(self):
        pass

class Select(Step):
    def __init__(self, p1, p2, **kwargs):