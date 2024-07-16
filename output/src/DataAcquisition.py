from mls.data_acquisition import LoadDataset
from mls.orchestration import Out, Step, Orchestrator

class DataAcquisition(Step):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.orchestrator = Orchestrator()
		load_dataset = LoadDataset(
			path = 'iris.csv',
			loader = 'local',
		)
		self.orchestrator.add(load_dataset)
		
		output = Out(
			key = 'dataset',
			value = (load_dataset, 'resulting_table'),
		)
		self.orchestrator.add(output)
		
		
	def execute(self):
		self.orchestrator.execute()
