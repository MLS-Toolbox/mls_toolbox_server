from mls.orchestration import Step, Out, In, Orchestrator
from mls.model_evaluation import Evaluate

class Evaluation(Step):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.orchestrator = Orchestrator()
		input = In(
			key = 'model',
		)
		self.orchestrator.add(input)
		
		input_2 = In(
			key = 'features',
		)
		self.orchestrator.add(input_2)
		
		input_3 = In(
			key = 'truth',
		)
		self.orchestrator.add(input_3)
		
		evaluate = Evaluate(
			# 
			description = '',
			model = (input, 'value'),
			features = (input_2, 'value'),
			truth = (input_3, 'value'),
		)
		self.orchestrator.add(evaluate)
		
		output = Out(
			key = 'results',
			value = (evaluate, 'result'),
		)
		self.orchestrator.add(output)
		
		
	def execute(self):
		self.orchestrator.execute()
