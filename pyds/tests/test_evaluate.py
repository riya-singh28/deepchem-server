"""
Unit tests for Evaluate primitive using live server.
"""

import os
import tempfile

import pytest

from pyds.data import Data
from pyds.primitives import Evaluate, Featurize, Train

class TestEvaluate:
    """Unit tests for Evaluate primitive."""

    def test_init(self, test_settings):
        """Test Evaluate initialization."""
        client = Evaluate(settings=test_settings)

        assert client.settings == test_settings
        assert client.base_url == "http://localhost:8000"

    def test_run_basic_validation(self, live_evaluate_client):
        """Test basic parameter validation on live server."""
        # Test with missing datasets to validate API communication
        with pytest.raises(Exception):
            live_evaluate_client.run(
                dataset_addresses=["non_existent_dataset"],
                model_address="non_existent_model",
                metrics=["accuracy"],
                output_key="test_evaluation",
            )

    def test_run_missing_settings(self, test_settings_not_configured):
        """Test evaluate run with missing settings."""
        client = Evaluate(settings=test_settings_not_configured)

        with pytest.raises(ValueError, match="Missing required settings"):
            client.run(
                dataset_addresses=["test/dataset"],
                model_address="test/model",
                metrics=["roc_auc_score"],
                output_key="evaluation_result",
            )
