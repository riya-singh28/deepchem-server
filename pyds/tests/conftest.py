"""
Pytest configuration and fixtures for pyds tests.
"""

import os
import tempfile

import pytest
import responses

from pyds import Settings
from pyds.base.client import BaseClient
from pyds.data import Data
from pyds.primitives import Evaluate, Featurize, Infer, Train

@pytest.fixture
def temp_settings_file():
    """Create a temporary settings file for testing."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        settings_file = f.name

    yield settings_file

    # Clean up
    if os.path.exists(settings_file):
        os.unlink(settings_file)

@pytest.fixture
def test_settings(temp_settings_file):
    """Create test settings instance."""
    settings = Settings(
        settings_file=temp_settings_file,
        profile="test_profile",
        project="test_project",
        base_url="http://localhost:8000",
    )
    return settings

@pytest.fixture
def test_settings_not_configured(temp_settings_file):
    """Create test settings instance without profile/project configured."""
    settings = Settings(settings_file=temp_settings_file, base_url="http://localhost:8000")
    return settings

@pytest.fixture
def base_client(test_settings):
    """Create BaseClient instance for testing."""
    return BaseClient(settings=test_settings)

@pytest.fixture
def featurize_client(test_settings):
    """Create Featurize primitive client for testing."""
    return Featurize(settings=test_settings)

@pytest.fixture
def train_client(test_settings):
    """Create Train primitive client for testing."""
    return Train(settings=test_settings)

@pytest.fixture
def evaluate_client(test_settings):
    """Create Evaluate primitive client for testing."""
    return Evaluate(settings=test_settings)

@pytest.fixture
def infer_client(test_settings):
    """Create Infer primitive client for testing."""
    return Infer(settings=test_settings)

@pytest.fixture
def data_client(test_settings):
    """Create Data client for testing."""
    return Data(settings=test_settings)

@pytest.fixture
def temp_test_file():
    """Create a temporary test file for upload testing."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("smiles,label\n")
        f.write("CCO,1\n")
        f.write("CCC,0\n")
        test_file = f.name

    yield test_file

    # Clean up
    if os.path.exists(test_file):
        os.unlink(test_file)

@pytest.fixture
def mock_responses():
    """Setup responses mock for HTTP requests."""
    with responses.RequestsMock() as rsps:
        yield rsps

@pytest.fixture
def sample_featurize_response():
    """Sample response for featurize endpoint."""
    return {"featurized_file_address": "test_profile/test_project/datasets/featurized_data"}

@pytest.fixture
def sample_train_response():
    """Sample response for train endpoint."""
    return {"trained_model_address": "test_profile/test_project/models/trained_model"}

@pytest.fixture
def sample_evaluate_response():
    """Sample response for evaluate endpoint."""
    return {"evaluation_result_address": "test_profile/test_project/evaluations/eval_result"}

@pytest.fixture
def sample_infer_response():
    """Sample response for infer endpoint."""
    return {"inference_results_address": "test_profile/test_project/predictions/infer_result"}

@pytest.fixture
def sample_upload_response():
    """Sample response for upload endpoint."""
    return {"dataset_address": "test_profile/test_project/datasets/uploaded_data"}

@pytest.fixture
def sample_healthcheck_response():
    """Sample response for healthcheck endpoint."""
    return {"status": "healthy", "version": "1.0.0"}

# Common test data fixtures
@pytest.fixture
def test_dataset_address():
    """Test dataset address."""
    return "test_profile/test_project/datasets/test_data"

@pytest.fixture
def test_model_address():
    """Test model address."""
    return "test_profile/test_project/models/test_model"

@pytest.fixture
def test_featurizer():
    """Test featurizer name."""
    return "CircularFingerprint"

@pytest.fixture
def test_model_type():
    """Test model type."""
    return "MultitaskClassifier"

@pytest.fixture
def test_metrics():
    """Test metrics list."""
    return ["roc_auc_score", "accuracy_score"]

# Live server testing fixtures
@pytest.fixture
def live_server_url():
    """URL for live server testing."""
    return os.getenv("PYDS_TEST_SERVER_URL", "http://localhost:8000")

@pytest.fixture
def live_settings(temp_settings_file, live_server_url):
    """Create settings for live server testing."""
    return Settings(
        settings_file=temp_settings_file,
        profile=os.getenv("PYDS_TEST_PROFILE", "test_profile"),
        project=os.getenv("PYDS_TEST_PROJECT", "test_project"),
        base_url=live_server_url,
    )

@pytest.fixture
def live_base_client(live_settings):
    """Create BaseClient for live server testing."""
    return BaseClient(settings=live_settings)

@pytest.fixture
def live_featurize_client(live_settings):
    """Create Featurize client for live server testing."""
    return Featurize(settings=live_settings)

@pytest.fixture
def live_train_client(live_settings):
    """Create Train client for live server testing."""
    return Train(settings=live_settings)

@pytest.fixture
def live_evaluate_client(live_settings):
    """Create Evaluate client for live server testing."""
    return Evaluate(settings=live_settings)

@pytest.fixture
def live_infer_client(live_settings):
    """Create Infer client for live server testing."""
    return Infer(settings=live_settings)

@pytest.fixture
def live_data_client(live_settings):
    """Create Data client for live server testing."""
    return Data(settings=live_settings)

def pytest_configure(config):
    """Configure pytest markers."""
    pass
