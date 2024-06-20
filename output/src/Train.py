from mls.orchestration import Out, In, Orchestrator
from mls.model_training.optimizers import Adam
from mls.model_training import TrainModel
from mls.model_training.models import LinearRegression

class Train(Orchestrator):
	def __init__(self, **kwargs):
		super.__init__(**kwargs)
		o = Orchestrator()
		
		input = In(
			key = 'features',
		)
		
		input_2 = In(
			key = 'truth',
		)
		
		optimizer = Adam(
			parameters = '',
		)
		
		mlmodel = LinearRegression(
			parameters = '',
		)
		
		train_model = TrainModel(
			epochs = '',
			bach_size = '',
			features = (input, 'value'),
			truth = (input_2, 'value'),
			optimizer = (optimizer, 'optimizer'),
			model = (mlmodel, 'model'),
		)
		
		output = Out(
			key = 'model',
			value = (train_model, 'model'),
		)
		
		o.add([input,input_2,optimizer,mlmodel,train_model,output])
		
