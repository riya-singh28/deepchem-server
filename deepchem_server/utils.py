from deepchem_server.core import config
from deepchem_server.core.datastore import DiskDataStore
from deepchem_server.core.compute import ComputeWorkflow


def run_job(profile_name: str,
            project_name: str,
            program: str,
            backend: str = 'local'):
    """
    """
    if backend == 'local':
        datastore = DiskDataStore(profile_name=profile_name,
                                  project_name=project_name)
        config.set_datastore(datastore)
        workflow = ComputeWorkflow(program)
        try:
            output = workflow.execute()
        except Exception as e:
            output = e
        return output
    else:
        raise NotImplementedError(f"{backend} backend not implemented")
