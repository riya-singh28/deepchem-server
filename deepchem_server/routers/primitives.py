import json
from typing import Optional, Dict
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from deepchem_server.utils import run_job
from deepchem_server.core.feat import featurizer_map

router = APIRouter(prefix="/primitive",
                   tags=["primitive"],)

@router.post("/featurize")
async def featurize(profile_name: str,
                    project_name: str,
                    dataset_address: str,
                    featurizer: str,
                    output: str,
                    dataset_column: str,
                    feat_kwargs: Dict = dict(),
                    label_column: Optional[str] = None,) -> Dict:
    """
    Submits a featurization job

    Parameters
    ----------
    profile_name: str
        Name of the Profile where the job is run
    project_name: str
        Name of the Project where the job is run
    dataset_address: str
        datastore address of dataset to featurize
    featurizer: str
        featurizer to use
    output: str
        name of the featurized dataset
    dataset_column: Optional[str]
        Column containing the input for featurizer
    feat_kwargs: Optional[Dict]
        Keyword arguments to pass to featurizer on initialization
    label_column: Optional[str]
        The target column in case this dataset is going to be used for training purposes
    """

    if featurizer not in featurizer_map.keys():
        return JSONResponse(status_code=404,
                            content={"message": "featurizer invalid"})

    if isinstance(feat_kwargs['feat_kwargs'], str):
        feat_kwargs['feat_kwargs'] = json.loads(feat_kwargs['feat_kwargs'])

    for key, value in feat_kwargs['feat_kwargs'].items():
        if isinstance(value, str):
            if value.lower() == "true":
                feat_kwargs['feat_kwargs'][key] = True
            elif value.lower() == "false":
                feat_kwargs['feat_kwargs'][key] = False
            elif value.lower() == "none":
                feat_kwargs['feat_kwargs'][key] = None

    program = {
        'program_name': 'featurize',
        'dataset_address': dataset_address,
        'featurizer': featurizer,
        'output': output,
        'dataset_column': dataset_column,
        'feat_kwargs': feat_kwargs['feat_kwargs'],
        'label_column': label_column,
    }

    output = run_job(profile_name=profile_name,
                     project_name=project_name,
                     program=program)

    return {"featurized_file_address": output}
