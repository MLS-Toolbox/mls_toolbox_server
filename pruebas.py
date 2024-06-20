
class Master:
    def __init__(self, **inputs):
        self.name = "Master"
        self.inputs = inputs
    
    def execute(self):
        print(self.inputs)

class Child(Master):
    def __init__(self, **inputs):
        super().__init__(**inputs)
        self.name = "Child"
        self.inputs = inputs


a = Master(
    param_1 = 1,
    param_2 = 2
)

b = Child(
    param_2 = 2,
    param_12 = 3
)

a.execute()
b.execute()