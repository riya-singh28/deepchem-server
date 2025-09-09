# Scripts Directory

This directory contains utility scripts for the DeepChem Server project.

## pytest_pyds.sh

A simple test runner script for the `pyds` package unit tests.

### Usage

```bash
# From project root
./scripts/pytest_pyds.sh
```

The script will:
1. Check that the `pyds` directory exists
2. Check that pytest is installed
3. Run all unit tests marked with `@pytest.mark.unit`
4. Report the results

### Prerequisites

- Python with pytest installed
- The script must be run from the project root directory

### What it does

The script runs unit tests only (not integration tests) using pytest with the `-m unit` marker. This ensures only isolated tests with mocked dependencies are executed, making it safe to run without requiring a live DeepChem server.

## Adding New Scripts

When adding new scripts to this directory:

1. Make them executable: `chmod +x script_name.sh`
2. Add proper documentation
3. Follow simple error handling patterns
4. Update this README