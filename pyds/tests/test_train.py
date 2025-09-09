"""
Unit tests for Train primitive using live server.
"""

import os
import tempfile
import time
import uuid

import pytest

from pyds.primitives import Train

class TestTrain:
    """Unit tests for Train primitive."""

    def test_init(self, test_settings):
        """Test Train initialization."""
        client = Train(settings=test_settings)

        assert client.settings == test_settings
        assert client.base_url == "http://localhost:8000"

    def test_train_random_forest_classifier(self, live_train_client, live_data_client, live_featurize_client):
        """Test training a random forest classifier with real data."""
        # Generate unique identifiers to avoid naming conflicts
        test_id = str(uuid.uuid4())[:8]
        timestamp = str(int(time.time()))

        # Create a classification dataset with enough diversity
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("smiles,label\n")
            # Create diverse molecular structures for classification
            molecules = [
                ("CCO", 1),  # ethanol
                ("CCC", 0),  # propane
                ("CCCO", 1),  # propanol
                ("CCCC", 0),  # butane
                ("CC(C)O", 1),  # isopropanol
                ("CC(C)C", 0),  # isobutane
                ("CCCCO", 1),  # butanol
                ("CCCCC", 0),  # pentane
                ("CC(C)CO", 1),  # isobutanol
                ("CC(C)(C)C", 0),  # neopentane
                ("CCCCCO", 1),  # pentanol
                ("CCCCCC", 0),  # hexane
                ("C(C(C)O)O", 1),  # ethylene glycol
                ("CCCCCCC", 0),  # heptane
                ("CCCCCCCO", 1),  # heptanol
            ]
            for smiles, label in molecules:
                f.write(f"{smiles},{label}\n")
            test_file = f.name

        try:
            # Upload data with unique filename
            upload_result = live_data_client.upload_data(
                file_path=test_file,
                filename=f"train_rf_cls_{test_id}_{timestamp}.csv",
                description="Test data for random forest classifier training",
            )

            # Featurize data using ECFP with unique output name
            featurize_result = live_featurize_client.run(
                dataset_address=upload_result["dataset_address"],
                featurizer="ecfp",
                output=f"train_rf_feat_{test_id}_{timestamp}",
                dataset_column="smiles",
                label_column="label",
                feat_kwargs={
                    "radius": 2,
                    "size": 1024
                },
            )

            # Train random forest classifier with unique model name
            result = live_train_client.run(
                dataset_address=featurize_result["featurized_file_address"],
                model_type="random_forest_classifier",
                model_name=f"rf_cls_model_{test_id}_{timestamp}",
                init_kwargs={
                    "n_estimators": 50,
                    "random_state": 42
                },
                train_kwargs={},
            )

            # Verify the response structure
            assert "trained_model_address" in result
            assert isinstance(result["trained_model_address"], str)
            assert len(result["trained_model_address"]) > 0

        finally:
            os.unlink(test_file)

    def test_train_random_forest_regressor(self, live_train_client, live_data_client, live_featurize_client):
        """Test training a random forest regressor with real data."""
        # Generate unique identifiers to avoid naming conflicts
        test_id = str(uuid.uuid4())[:8]
        timestamp = str(int(time.time()))

        # Create a regression dataset
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("smiles,target\n")
            # Create molecules with continuous target values (e.g., molecular weight proxy)
            molecules = [
                ("C", 0.5),  # methane (smallest)
                ("CC", 1.0),  # ethane
                ("CCC", 1.5),  # propane
                ("CCCC", 2.0),  # butane
                ("CCCCC", 2.5),  # pentane
                ("CCO", 1.2),  # ethanol
                ("CCCO", 1.7),  # propanol
                ("CCCCO", 2.2),  # butanol
                ("CC(C)C", 2.1),  # isobutane
                ("CC(C)O", 1.6),  # isopropanol
                ("CCCCCC", 3.0),  # hexane
                ("CCCCCCC", 3.5),  # heptane
            ]
            for smiles, target in molecules:
                f.write(f"{smiles},{target}\n")
            test_file = f.name

        try:
            # Upload data with unique filename
            upload_result = live_data_client.upload_data(
                file_path=test_file,
                filename=f"train_rf_reg_{test_id}_{timestamp}.csv",
                description="Test data for random forest regressor training",
            )

            # Featurize data with unique output name
            featurize_result = live_featurize_client.run(
                dataset_address=upload_result["dataset_address"],
                featurizer="ecfp",
                output=f"train_rf_reg_feat_{test_id}_{timestamp}",
                dataset_column="smiles",
                label_column="target",
                feat_kwargs={
                    "radius": 2,
                    "size": 512
                },
            )

            # Train random forest regressor with unique model name
            result = live_train_client.run(
                dataset_address=featurize_result["featurized_file_address"],
                model_type="random_forest_regressor",
                model_name=f"rf_reg_model_{test_id}_{timestamp}",
                init_kwargs={
                    "n_estimators": 30,
                    "random_state": 42
                },
                train_kwargs={},
            )

            # Verify the response structure
            assert "trained_model_address" in result
            assert isinstance(result["trained_model_address"], str)
            assert len(result["trained_model_address"]) > 0

        finally:
            os.unlink(test_file)

    def test_train_linear_regression(self, live_train_client, live_data_client, live_featurize_client):
        """Test training a linear regression model with real data."""
        # Generate unique identifiers to avoid naming conflicts
        test_id = str(uuid.uuid4())[:8]
        timestamp = str(int(time.time()))

        # Create a simple regression dataset
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("smiles,property\n")
            # Simple molecules with a linear relationship to carbon count
            molecules = [
                ("C", 1.0),
                ("CC", 2.0),
                ("CCC", 3.0),
                ("CCCC", 4.0),
                ("CCCCC", 5.0),
                ("CCCCCC", 6.0),
                ("CO", 1.5),
                ("CCO", 2.5),
                ("CCCO", 3.5),
            ]
            for smiles, prop in molecules:
                f.write(f"{smiles},{prop}\n")
            test_file = f.name

        try:
            # Upload and featurize data with unique names
            upload_result = live_data_client.upload_data(
                file_path=test_file,
                filename=f"train_linear_reg_{test_id}_{timestamp}.csv",
                description="Test data for linear regression training",
            )

            featurize_result = live_featurize_client.run(
                dataset_address=upload_result["dataset_address"],
                featurizer="ecfp",
                output=f"train_linear_feat_{test_id}_{timestamp}",
                dataset_column="smiles",
                label_column="property",
            )

            # Train linear regression model with unique name
            result = live_train_client.run(
                dataset_address=featurize_result["featurized_file_address"],
                model_type="linear_regression",
                model_name=f"linear_model_{test_id}_{timestamp}",
                init_kwargs={"fit_intercept": True},
                train_kwargs={},
            )

            # Verify the response structure
            assert "trained_model_address" in result
            assert isinstance(result["trained_model_address"], str)
            assert len(result["trained_model_address"]) > 0

        finally:
            os.unlink(test_file)

    def test_train_with_minimal_parameters(self, live_train_client, live_data_client, live_featurize_client):
        """Test training with minimal parameters (using defaults)."""
        # Generate unique identifiers to avoid naming conflicts
        test_id = str(uuid.uuid4())[:8]
        timestamp = str(int(time.time()))

        # Create minimal dataset
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("smiles,label\n")
            f.write("CCO,1\n")
            f.write("CCC,0\n")
            f.write("CCCO,1\n")
            f.write("CCCC,0\n")
            f.write("CCCCO,1\n")
            test_file = f.name

        try:
            # Upload and featurize with unique names
            upload_result = live_data_client.upload_data(
                file_path=test_file,
                filename=f"train_minimal_{test_id}_{timestamp}.csv",
            )

            featurize_result = live_featurize_client.run(
                dataset_address=upload_result["dataset_address"],
                featurizer="ecfp",
                output=f"train_minimal_feat_{test_id}_{timestamp}",
                dataset_column="smiles",
                label_column="label",
            )

            # Train with minimal parameters (no init_kwargs, no train_kwargs)
            result = live_train_client.run(
                dataset_address=featurize_result["featurized_file_address"],
                model_type="random_forest_classifier",
                model_name=f"minimal_model_{test_id}_{timestamp}",
            )

            # Verify response
            assert "trained_model_address" in result
            assert isinstance(result["trained_model_address"], str)

        finally:
            os.unlink(test_file)

    def test_train_invalid_model_type(self, live_train_client):
        """Test training with invalid model type."""
        with pytest.raises(Exception, match="Invalid model type"):
            live_train_client.run(
                dataset_address="test/dataset",
                model_type="NonExistentModel",
                model_name="test_model",
            )

    def test_train_nonexistent_dataset(self, live_train_client):
        """Test training with non-existent dataset."""
        with pytest.raises(Exception):
            live_train_client.run(
                dataset_address="nonexistent/dataset/address",
                model_type="random_forest_classifier",
                model_name="test_model",
            )

    def test_run_missing_settings(self, test_settings_not_configured):
        """Test train run with missing settings."""
        client = Train(settings=test_settings_not_configured)

        with pytest.raises(ValueError, match="Missing required settings"):
            client.run(
                dataset_address="test/dataset",
                model_type="random_forest_classifier",
                model_name="trained_model",
            )
