from mls.data_transformation import IDataTransformation

class Join(IDataTransformation):
    def __init__(self, left, right, on, how):
        super().__init__()
        self.left = left
        self.right = right
        self.on = on
        self.how = how

    def execute(self):
        pass