from mls.data_acquisition import LoadDataset
from mls.orchestration import Out, Orchestrator

class DataAcquisition(Orchestrator):
	def __init__(self, **kwargs):
		super.__init__(self)
		o = Orchestrator()
		
		load_dataset = LoadDataset(
			path = 'iris.csv',
			loader = 'local',
		)
		
		output = Out(
			key = 'dataset',
			value = (load_dataset, 'resulting_table'),
		)
		
		o.add([load_dataset,output])
		
