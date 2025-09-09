"""
Unit tests for Featurize primitive using live server.
"""

import os
import tempfile

import pytest

from pyds.primitives import Featurize

class TestFeaturize:
    """Unit tests for Featurize primitive."""

    def test_init(self, test_settings):
        """Test Featurize initialization."""
        client = Featurize(settings=test_settings)

        assert client.settings == test_settings
        assert client.base_url == "http://localhost:8000"

    def test_run_success(self, live_featurize_client, live_data_client):
        """Test successful featurize run on live server."""
        # Upload test data first
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("smiles,label\n")
            f.write("CCO,1\n")
            f.write("CCC,0\n")
            f.write("CCCO,1\n")
            test_file = f.name

        try:
            # Upload data
            upload_result = live_data_client.upload_data(
                file_path=test_file,
                filename="test_featurize.csv",
                description="Test data for featurization",
            )
            dataset_address = upload_result["dataset_address"]

            # Test featurization
            result = live_featurize_client.run(
                dataset_address=dataset_address,
                featurizer="ecfp",
                output="test_featurized_output",
                dataset_column="smiles",
                feat_kwargs={
                    "radius": 2,
                    "size": 1024
                },
                label_column="label",
            )

            assert "featurized_file_address" in result
        finally:
            os.unlink(test_file)

    def test_run_with_defaults(self, live_featurize_client, live_data_client):
        """Test featurize run with default parameters on live server."""
        # Upload test data first
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("smiles,label\n")
            f.write("CCO,1\n")
            f.write("CCC,0\n")
            test_file = f.name

        try:
            # Upload data
            upload_result = live_data_client.upload_data(
                file_path=test_file,
                filename="test_featurize_defaults.csv",
                description="Test data for featurization with defaults",
            )
            dataset_address = upload_result["dataset_address"]

            # Test featurization with minimal parameters
            result = live_featurize_client.run(
                dataset_address=dataset_address,
                featurizer="ecfp",
                output="test_featurized_defaults",
                dataset_column="smiles",
            )

            assert "featurized_file_address" in result
        finally:
            os.unlink(test_file)

    def test_run_with_profile_project_override(self, live_featurize_client, live_data_client):
        """Test featurize run with profile and project override on live server."""
        # Upload test data first
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("smiles,label\n")
            f.write("CCO,1\n")
            f.write("CCC,0\n")
            test_file = f.name

        try:
            # Upload data
            upload_result = live_data_client.upload_data(
                file_path=test_file,
                filename="test_featurize_override.csv",
                description="Test data for featurization with override",
            )
            dataset_address = upload_result["dataset_address"]

            # Test featurization with profile/project override
            result = live_featurize_client.run(
                dataset_address=dataset_address,
                featurizer="ecfp",
                output="test_featurized_override",
                dataset_column="smiles",
                profile_name="test_profile",
                project_name="test_project",
            )

            assert "featurized_file_address" in result
        finally:
            os.unlink(test_file)

    def test_run_missing_settings(self, test_settings_not_configured):
        """Test featurize run with missing settings."""
        client = Featurize(settings=test_settings_not_configured)

        with pytest.raises(ValueError, match="Missing required settings"):
            client.run(
                dataset_address="test/dataset",
                featurizer="CircularFingerprint",
                output="featurized_output",
                dataset_column="smiles",
            )

    def test_run_api_error(self, live_featurize_client):
        """Test featurize run with API error on live server."""
        # Test with invalid featurizer to trigger server error
        with pytest.raises(Exception, match="Invalid featurizer"):
            live_featurize_client.run(
                dataset_address="test/dataset",
                featurizer="InvalidFeaturizer",
                output="featurized_output",
                dataset_column="smiles",
            )
