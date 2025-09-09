# PyDS Test Suite

This directory contains comprehensive unit tests and integration tests for the `pyds` package.

## Test Structure

```
tests/
├── __init__.py                 # Test package initialization
├── conftest.py                 # Pytest configuration and fixtures
├── test_base_client.py         # Tests for BaseClient class
├── test_settings.py            # Tests for Settings class
├── test_data.py                # Tests for Data class
├── test_featurize.py           # Tests for Featurize primitive
├── test_train.py               # Tests for Train primitive
├── test_evaluate.py            # Tests for Evaluate primitive
├── test_infer.py               # Tests for Infer primitive
├── test_integration.py         # Integration tests against live server
├── test_utils.py               # Test utilities and helpers
└── README.md                   # This file
```

## Test Types

### Unit Tests
- **Marker**: `@pytest.mark.unit`
- **Description**: Test individual methods and classes in isolation using mocks
- **Requirements**: No external dependencies (no running server needed)
- **Coverage**: All public methods, error conditions, edge cases

### Integration Tests
- **Marker**: `@pytest.mark.integration`
- **Description**: Test complete workflows against a live DeepChem server
- **Requirements**: Running DeepChem server
- **Coverage**: End-to-end workflows, real API interactions

### Stress Tests
- **Marker**: `@pytest.mark.slow`
- **Description**: Test system behavior under load
- **Requirements**: Running DeepChem server, longer execution time

## Running Tests

### Prerequisites

1. **Install test dependencies**:
   ```bash
   pip install -r requirements-dev.txt
   ```

2. **For integration tests**, ensure DeepChem server is running:
   ```bash
   # Start the server (adjust command as needed)
   python -m deepchem_server.main
   ```

### Quick Start

```bash
# Run all tests with coverage
../scripts/pytest_pyds.sh all --coverage

# Run only unit tests
../scripts/pytest_pyds.sh unit

# Run only integration tests (requires server)
../scripts/pytest_pyds.sh integration

# Check if server is available
../scripts/pytest_pyds.sh check-server
```

### Detailed Usage

#### Using pytest directly

```bash
# Run all tests
pytest tests/

# Run unit tests only
pytest -m unit tests/

# Run integration tests only
pytest -m integration tests/

# Run with coverage
pytest --cov=pyds --cov-report=html --cov-report=term tests/

# Run specific test file
pytest tests/test_featurize.py

# Run tests matching pattern
pytest -k "test_upload" tests/

# Verbose output
pytest -v tests/
```

#### Using the test runner script

```bash
# Show help
../scripts/pytest_pyds.sh help

# Run unit tests with verbose output
../scripts/pytest_pyds.sh unit -v

# Run integration tests
../scripts/pytest_pyds.sh integration

# Generate coverage report
../scripts/pytest_pyds.sh coverage

# Run specific test pattern
../scripts/pytest_pyds.sh pattern "featurize"

# Check code quality
../scripts/pytest_pyds.sh lint

# Format code
../scripts/pytest_pyds.sh format
```

## Environment Configuration

### Environment Variables

For integration tests, you can configure:

```bash
export PYDS_TEST_SERVER_URL="http://localhost:8000"
export PYDS_TEST_PROFILE="test_profile"
export PYDS_TEST_PROJECT="test_project"
```

### Test Settings

Tests use temporary settings files to avoid conflicts with your actual configuration.

## Coverage Configuration

Coverage is configured via `.coveragerc` in the package root:

- **Source**: `pyds` package
- **Omit**: Test files, cache files, setup files
- **Target**: 75% minimum coverage
- **Reports**: HTML, terminal, and XML formats

### Coverage Reports

After running tests with coverage:

- **HTML Report**: `htmlcov/index.html`
- **XML Report**: `coverage.xml`
- **Terminal**: Displayed after test run

## Test Fixtures

The `conftest.py` file provides numerous fixtures:

### Settings Fixtures
- `test_settings`: Configured settings for testing
- `test_settings_not_configured`: Settings without profile/project
- `temp_settings_file`: Temporary settings file

### Client Fixtures
- `base_client`: BaseClient instance
- `featurize_client`: Featurize primitive client
- `train_client`: Train primitive client
- `evaluate_client`: Evaluate primitive client
- `infer_client`: Infer primitive client
- `data_client`: Data client

### Live Server Fixtures
- `live_*_client`: Client instances for integration tests
- `live_settings`: Settings configured for live server testing

### Test Data Fixtures
- `temp_test_file`: Temporary CSV file with test data
- `sample_*_response`: Mock API responses
- `test_*_address`: Test addresses and identifiers

## Writing New Tests

### Unit Test Example

```python
import pytest
import responses
from pyds.primitives import Featurize

@pytest.mark.unit
class TestFeaturize:
    @responses.activate
    def test_run_success(self, featurize_client, sample_featurize_response):
        responses.add(
            responses.POST,
            "http://localhost:8000/primitive/featurize",
            json=sample_featurize_response,
            status=200
        )
        
        result = featurize_client.run(
            dataset_address="test/dataset",
            featurizer="CircularFingerprint",
            output="test_output",
            dataset_column="smiles"
        )
        
        assert result == sample_featurize_response
```

### Integration Test Example

```python
import pytest
from pyds.data import Data

@pytest.mark.integration
class TestDataIntegration:
    def test_upload_workflow(self, live_data_client, temp_test_file):
        try:
            result = live_data_client.upload_data(
                file_path=temp_test_file,
                filename="test.csv",
                description="Integration test"
            )
            
            assert "dataset_address" in result
            
        except Exception as e:
            pytest.skip(f"Server not available: {e}")
```

## Best Practices

### Test Organization
1. **One test class per class being tested**
2. **Group related tests together**
3. **Use descriptive test names**
4. **Test both success and failure cases**

### Mocking
1. **Mock external dependencies in unit tests**
2. **Use `responses` library for HTTP mocking**
3. **Don't mock the code you're testing**

### Integration Tests
1. **Always handle server unavailability gracefully**
2. **Use `pytest.skip()` when server is not available**
3. **Clean up test data when possible**
4. **Make tests independent of each other**

### Error Handling
1. **Test error conditions**
2. **Verify proper exception types and messages**
3. **Test edge cases and boundary conditions**

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      
      - name: Install dependencies
        run: |
          pip install -r requirements-dev.txt
      
      - name: Run unit tests
        run: python tests/run_tests.py --unit --coverage
      
      - name: Upload coverage
        uses: codecov/codecov-action@v1
```

## Troubleshooting

### Common Issues

1. **Server not available for integration tests**
   - Ensure DeepChem server is running
   - Check `PYDS_TEST_SERVER_URL` environment variable
   - Use `--check-server` to verify connectivity

2. **Coverage reports not generated**
   - Ensure `pytest-cov` is installed
   - Check `.coveragerc` configuration
   - Verify source paths are correct

3. **Tests failing with permission errors**
   - Check file permissions on temporary files
   - Ensure test directory is writable

4. **Import errors**
   - Ensure `pyds` package is installed in development mode
   - Check Python path and virtual environment

### Debug Mode

Run tests with additional debugging:

```bash
# Verbose pytest output
pytest -vv -s tests/

# Show local variables on failure
pytest --tb=long tests/

# Drop into debugger on failure
pytest --pdb tests/
```

## Contributing

When adding new features to `pyds`:

1. **Write unit tests first** (TDD approach)
2. **Add integration tests** for end-to-end workflows
3. **Update fixtures** if new test data is needed
4. **Run full test suite** before submitting PR
5. **Ensure coverage** meets minimum threshold

### Test Checklist

- [ ] Unit tests for all public methods
- [ ] Integration tests for workflows
- [ ] Error condition testing
- [ ] Edge case coverage
- [ ] Documentation updated
- [ ] Coverage target met