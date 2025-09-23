"""
Train-Valid-Test Split primitive module for DeepChem Server.

Contains the TvtSplit class for splitter tasks.
"""

from typing import Dict, Optional

from .base import Primitive

class TvtSplit(Primitive):
    """
    Primitive for Train-Valid-Test Split tasks.

    This class handles submitting train-valid-test split jobs to the DeepChem Server API.
    """
    def run(
            self,
            splitter_type: str,
            dataset_address: str,
            frac_train: float = 0.8,
            frac_test: float = 0.1,
            frac_valid: float = 0.1,
            profile_name: Optional[str] = None,
            project_name: Optional[str] = None,) -> Dict:
        """
        Performs train test validation split on a dataset

        Args:
            splitter_type: Splitter type to use when splitting dataset.
            dataset_address: Dataset to perform splitting
            frac_train: Fraction of training dataset
            frac_test: Fraction of testing dataset
            frac_valid: Fraction of validation dataset
            job_config_id: Job configuriton id

        Returns:
            Response containing the split result address

        Raises:
            ValueError: If required settings are missing
            requests.exceptions.RequestException: If API request fails


        .. list-table:: Supported splitters
          :widths: 25 50
          :header-rows: 1

          * - Splitter type
            - Description
          * - random
            - Splits data into random subsets
          * - index
            - Splits data into subsets by index
          * - scaffold
            - Splits data into subsets using scaffolds
        """
        profile, project = self.validate_common_params(profile_name, project_name)
        data = {
            "profile_name": profile,
            "project_name": project,
            'splitter_type': splitter_type,
            'dataset_address': dataset_address,
            'frac_train': frac_train,
            'frac_valid': frac_valid,
            'frac_test': frac_test,
        }
        api_path = "/primitive/train-valid-test-split"
        response = self._post(api_path, json=data)
        return self._validate_response(response)
