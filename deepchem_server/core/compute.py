import deepchem_server.core as core
from typing import Any, Dict

program_map = {'featurize': core.featurize}


class ComputeWorkflow:
    """A Compute Workflow is a workflow that runs on Deepchem Server.

    Examples
    --------
    >>> program = program = {
    ... 'program_name': 'featurize',
    ... 'dataset_address': 'deepchem://profile_name/project_name/data.csv',
    ... 'featurizer': 'ecfp',
    ... 'output': 'test_output',
    ... 'dataset_column': 'smiles',
    ... 'feat_kwargs': {'size': 1024},
    ... 'label_column': 'y',
    ... }
    """

    def __init__(self, program: Dict):
        """Initialize Worfklow."""
        self.program: Dict = program

    def execute(self) -> Any:
        """Runs the program in Dictionary format based on  `program_name` in program"""
        if 'program_name' not in self.program:
            raise ValueError("program_name not found in program")
        program_name: str = self.program['program_name']
        params: Dict = {
            key: value
            for key, value in self.program.items()
            if key != 'program_name'
        }
        if program_name not in program_map:
            raise ValueError(f"{program_name} not in available programs")

        output: Any = program_map[program_name](**params)
        return output
