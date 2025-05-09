"""
Utility functions required by app for performing operations
"""
import uuid
from deepchem_server.core import config
from deepchem_server.core.datastore import DiskDataStore


def run_job(profile_name: str,
            project_name: str,
            program: str,
            backend: str = 'local'):
    """
    """
    if backend == 'aws':
        raise NotImplementedError

    elif backend == 'local':
        datastore = DiskDataStore(profile_name=profile_name,
                                  project_name=project_name)
        config.set_datastore(datastore)
        workflow = ComputeWorkflow(program)
        workflow.execute()
        job_id = uuid.uuid1().hex
        return job_id
