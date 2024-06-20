from mls.orchestration import Out, In, Orchestrator
from mls.data_preprocessing import TrainEncoder, TrainScaler, ReplaceNan
from mls.data_transformation import DropColumns
from mls.encoders import OneHotEncoder
from mls.scalers import Standard

class DataPreProcessing(Orchestrator):
	def __init__(self, **kwargs):
		super.__init__(self)
		o = Orchestrator()
		
		input = In(
			key = 'dataset',
		)
		
		replace_nan = ReplaceNan(
			value = '',
			origin = (input, 'value'),
		)
		
		drop_columns = DropColumns(
			columns = 'ID_x',
			origin_table = (replace_nan, 'result'),
		)
		
		encoder = OneHotEncoder(
			parmeters = '',
		)
		
		scaler = Standard(
			parmeters = '',
		)
		
		trainencoder = TrainEncoder(
			columns = '',
			encoder = (encoder, 'encoder'),
			data = (drop_columns, 'resulting_table'),
		)
		
		trainscaler = TrainScaler(
			columns = '',
			data = (trainencoder, 'out'),
			scaler = (scaler, 'scaler'),
		)
		
		output = Out(
			key = 'data',
			value = (trainscaler, 'data'),
		)
		
		output_2 = Out(
			key = 'scaler',
			value = (trainscaler, 'scaler'),
		)
		
		output_3 = Out(
			key = 'encoder',
			value = (trainencoder, 'encoder'),
		)
		
		o.add([input,replace_nan,drop_columns,encoder,scaler,trainencoder,trainscaler,output,output_2,output_3])
		
