from mls.orchestration import Orchestrator, Out, In, StepManager, Step
from mls.data_transformation import SplitTrainTest, SelectColumns

class DataTransformation(Step):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.orchestrator = Orchestrator()
		input = In(
			key = 'data',
		)
		self.orchestrator.add(input)
		
		select_columns = SelectColumns(
			columns = '',
			origin_table = (input, 'value'),
		)
		self.orchestrator.add(select_columns)
		
		select_columns_2 = SelectColumns(
			columns = '',
			origin_table = (input, 'value'),
		)
		self.orchestrator.add(select_columns_2)
		
		split_train_test = SplitTrainTest(
			train_percentage = '',
			features = (select_columns, 'resulting_table'),
			truth = (select_columns_2, 'resulting_table'),
		)
		self.orchestrator.add(split_train_test)
		
		output = Out(
			key = 'features_train',
			value = (split_train_test, 'features_train'),
		)
		self.orchestrator.add(output)
		
		output_2 = Out(
			key = 'features_test',
			value = (split_train_test, 'features_test'),
		)
		self.orchestrator.add(output_2)
		
		output_3 = Out(
			key = 'truth_train',
			value = (split_train_test, 'truth_train'),
		)
		self.orchestrator.add(output_3)
		
		output_4 = Out(
			key = 'truth_test',
			value = (split_train_test, 'truth_test'),
		)
		self.orchestrator.add(output_4)
		
		
	def execute(self):
		self.orchestrator.execute()
