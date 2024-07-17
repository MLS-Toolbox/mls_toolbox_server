from mls.orchestration import In, Step, Orchestrator, Out
from mls.data_preprocessing import ReplaceNan, TrainScaler, TrainEncoder
from mls.data_transformation import DropColumns
from mls.encoders import OneHotEncoder
from mls.scalers import Standard

class DataPreProcessing(Step):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.orchestrator = Orchestrator()
		input = In(
			key = 'dataset',
		)
		self.orchestrator.add(input)
		
		replace_nan = ReplaceNan(
			value = '',
			origin = (input, 'value'),
		)
		self.orchestrator.add(replace_nan)
		
		# dropped X columns
		drop_columns = DropColumns(
			columns = 'ID_x',
			origin_table = (replace_nan, 'result'),
		)
		self.orchestrator.add(drop_columns)
		
		encoder = OneHotEncoder(
			parmeters = '',
		)
		
		self.orchestrator.add(encoder)
		
		scaler = Standard(
			parmeters = '',
		)
		self.orchestrator.add(scaler)
		
		trainencoder = TrainEncoder(
			columns = '',
			encoder = (encoder, 'encoder'),
			data = (drop_columns, 'resulting_table'),
		)
		self.orchestrator.add(trainencoder)
		
		trainscaler = TrainScaler(
			columns = '',
			data = (trainencoder, 'out'),
			scaler = (scaler, 'scaler'),
		)
		self.orchestrator.add(trainscaler)
		
		output = Out(
			key = 'data',
			value = (trainscaler, 'data'),
		)
		self.orchestrator.add(output)
		
		output_2 = Out(
			key = 'scaler',
			value = (trainscaler, 'scaler'),
		)
		self.orchestrator.add(output_2)
		
		output_3 = Out(
			key = 'encoder',
			value = (trainencoder, 'encoder'),
		)
		self.orchestrator.add(output_3)
		
		
	def execute(self):
		self.orchestrator.execute()
