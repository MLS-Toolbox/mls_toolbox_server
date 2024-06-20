from mls.orchestration import Out, In, StepManager, Orchestrator
from mls.data_transformation import SelectColumns, SplitTrainTest

class DataTransformation(Orchestrator):
	def __init__(self, **kwargs):
		super.__init__(**kwargs)
		o = Orchestrator()
		
		input = In(
			key = 'data',
		)
		
		select_columns = SelectColumns(
			columns = '',
			origin_table = (input, 'value'),
		)
		
		select_columns_2 = SelectColumns(
			columns = '',
			origin_table = (input, 'value'),
		)
		
		split_train_test = SplitTrainTest(
			train_percentage = '',
			features = (select_columns, 'resulting_table'),
			truth = (select_columns_2, 'resulting_table'),
		)
		
		output = Out(
			key = 'features_train',
			value = (split_train_test, 'features_train'),
		)
		
		output_2 = Out(
			key = 'features_test',
			value = (split_train_test, 'features_test'),
		)
		
		output_3 = Out(
			key = 'truth_train',
			value = (split_train_test, 'truth_train'),
		)
		
		output_4 = Out(
			key = 'truth_test',
			value = (split_train_test, 'truth_test'),
		)
		
		o.add([input,select_columns,select_columns_2,split_train_test,output,output_2,output_3,output_4])
		
