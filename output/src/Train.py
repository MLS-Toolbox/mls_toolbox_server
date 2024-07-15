from mls.orchestration import Step, Out, In, Orchestrator
from mls.model_training.optimizers import Adam
from mls.model_training import TrainModel
from mls.model_training.models import LinearRegression

class Train(Step):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.orchestrator = Orchestrator()
		input = In(
			key = 'features',
		)
		self.orchestrator.add(input)
		
		input_2 = In(
			key = 'truth',
		)
		self.orchestrator.add(input_2)
		
		optimizer = Adam(
			# 
			description = '',
			parameters = '',
		)
		self.orchestrator.add(optimizer)
		
		mlmodel = LinearRegression(
			# 
			description = '',
			parameters = '',
		)
		self.orchestrator.add(mlmodel)
		
		train_model = TrainModel(
			# 
			description = '',
			epochs = '',
			bach_size = '',
			features = (input, 'value'),
			truth = (input_2, 'value'),
			optimizer = (optimizer, 'optimizer'),
			model = (mlmodel, 'model'),
		)
		self.orchestrator.add(train_model)
		
		output = Out(
			key = 'model',
			value = (train_model, 'model'),
		)
		self.orchestrator.add(output)
		
		
	def execute(self):
		self.orchestrator.execute()
