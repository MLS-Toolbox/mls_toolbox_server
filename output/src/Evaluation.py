from mls.orchestration import Out, In, Orchestrator
from mls.model_evaluation import Evaluate

class Evaluation(Orchestrator):
	def __init__(self, **kwargs):
		super.__init__(self)
		o = Orchestrator()
		
		input = In(
			key = 'model',
		)
		
		input_2 = In(
			key = 'features',
		)
		
		input_3 = In(
			key = 'truth',
		)
		
		evaluate = Evaluate(
			model = (input, 'value'),
			features = (input_2, 'value'),
			truth = (input_3, 'value'),
		)
		
		output = Out(
			key = 'results',
			value = (evaluate, 'result'),
		)
		
		o.add([input,input_2,input_3,evaluate,output])
		
