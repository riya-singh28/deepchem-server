"""
Unit tests for Infer primitive using live server.
"""

import pytest

from pyds.primitives import Infer

class TestInfer:
    """Unit tests for Infer primitive."""

    def test_init(self, test_settings):
        """Test Infer initialization."""
        client = Infer(settings=test_settings)

        assert client.settings == test_settings
        assert client.base_url == "http://localhost:8000"

    def test_run_basic_validation(self, live_infer_client):
        """Test basic parameter validation on live server."""
        # Test with missing model to validate API communication
        with pytest.raises(Exception):
            live_infer_client.run(
                model_address="non_existent_model",
                data_address="non_existent_data",
                output="test_inference",
            )

    def test_run_missing_settings(self, test_settings_not_configured):
        """Test infer run with missing settings."""
        client = Infer(settings=test_settings_not_configured)

        with pytest.raises(ValueError, match="Missing required settings"):
            client.run(
                model_address="test/model",
                data_address="test/data",
                output="inference_output",
            )
