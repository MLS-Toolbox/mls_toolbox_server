from mls.orchestration import Step

class In(Step):
    def __init__(self, key):
        super.__init__(self)
        self.key = key
    
    def exec(self):
        pass
