import datetime as dt
import json
from typing import Optional, Dict
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from deepchem_server.utils import run_job

COST_CONSTANT = 0.01

router = APIRouter(prefix="/primitive",
                   tags=["primitive"],)

@router.post("/featurize")
async def featurize(dataset_address: str,
                    featurizer: str,
                    output_key: str,
                    node_id: str = None,
                    job_config_id: str = 'cjc-10',
                    use_ray: bool = False,
                    dataset_column: Optional[str] = None,
                    feat_kwargs: Optional[Dict] = dict(),
                    label_column: Optional[str] = None):
    """
    Submits a featurization job

    Parameters
    ----------
    dataset_address: str
        dataset address of dataset to featurize
    featurizer: str
        featurizer to use
    output_key: str
        name of the featurized dataset
    job_config_id: str
        job configuration id (default: 'cjc-10')
    dataset_column: Optional[str]
        Column containing the input for featurizer
    feat_kwargs: Optional[Dict]
        Keyword arguments to pass to featurizer on initialization
    label_column: Optional[str]
        The target column in case this dataset is going to be used for training purposes
    use_ray: bool, default: False
        If set to True, use ray for featurizing dataset
    """
    try:
        dataset_address = process_address(dataset_address, project,
                                          current_user, db)
    except AssertionError:
        raise HTTPException(status_code=422,
                            detail=f"invalid dataset address {dataset_address}")
    if use_ray:
        job_id = submit_ray_featurization_job(dataset_address,
                                              output_key,
                                              featurizer,
                                              dataset_column,
                                              project=project)
        return JSONResponse(status_code=200,
                            content={
                                'status': 'ok',
                                'job_id': job_id
                            })
    # TODO Check for valid job config id
    if featurizer not in mappings.featurizer_map.keys():
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

    program = """
    featurized_address = featurize("%s", "%s", "%s", "%s", "%s", "%s")
    """ % (dataset_address, featurizer, output_key, dataset_column,
           str(feat_kwargs['feat_kwargs']), label_column)

    # TODO Function call for individual cost for each primitive
    datastore = _init_datastore(project)
    config.set_datastore(datastore)

    job_id = run_job(project,
                     program,
                     job_config_id=job_config_id,
                     node_id=node_id)
    if job_id is None:
        raise HTTPException(status_code=400, detail='invalid job configuration')
    return {"job_id": job_id}
