"""
Test utilities and helper functions.
"""

import json
import os
from pathlib import Path
import tempfile
from typing import Any, Dict

def create_test_csv_file(data_rows: list, headers: list = None, suffix: str = ".csv") -> str:
    """
    Create a temporary CSV file with test data.

    Args:
        data_rows: List of data rows to write
        headers: Column headers (default: ["smiles", "label"])
        suffix: File suffix (default: .csv)

    Returns:
        Path to the created temporary file
    """
    if headers is None:
        headers = ["smiles", "label"]

    with tempfile.NamedTemporaryFile(mode="w", suffix=suffix, delete=False) as f:
        # Write headers
        f.write(",".join(headers) + "\n")

        # Write data rows
        for row in data_rows:
            if isinstance(row, (list, tuple)):
                f.write(",".join(str(item) for item in row) + "\n")
            else:
                f.write(str(row) + "\n")

        return f.name

def create_test_sdf_file(molecules: list, suffix: str = ".sdf") -> str:
    """
    Create a temporary SDF file with test molecules.

    Args:
        molecules: List of molecule data (simplified for testing)
        suffix: File suffix (default: .sdf)

    Returns:
        Path to the created temporary file
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=suffix, delete=False) as f:
        for i, mol in enumerate(molecules):
            f.write(f"Molecule_{i}\n")
            f.write("  -OEChem-01010000002D\n")
            f.write(f"  {len(mol)} 0  0     0  0            999 V2000\n")
            f.write(f"{mol}\n")
            f.write("M  END\n")
            f.write("$$$$\n")

        return f.name

def cleanup_temp_file(file_path: str) -> None:
    """
    Clean up a temporary file.

    Args:
        file_path: Path to the file to remove
    """
    try:
        if os.path.exists(file_path):
            os.unlink(file_path)
    except Exception:
        pass  # Ignore cleanup errors

def create_test_settings_file(profile: str = None, project: str = None, base_url: str = None, **kwargs) -> str:
    """
    Create a temporary settings file for testing.

    Args:
        profile: Profile name
        project: Project name
        base_url: Base URL
        **kwargs: Additional settings

    Returns:
        Path to the created settings file
    """
    settings_data = {
        "profile": profile,
        "project": project,
        "base_url": base_url or "http://localhost:8000",
        "additional_settings": kwargs,
    }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(settings_data, f, indent=2)
        return f.name

def mock_api_response(status_code: int = 200, data: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Create a mock API response.

    Args:
        status_code: HTTP status code
        data: Response data

    Returns:
        Mock response data
    """
    if data is None:
        data = {"status": "success"}

    return {"status_code": status_code, "json": data}

def generate_test_smiles(count: int = 10) -> list:
    """
    Generate test SMILES strings.

    Args:
        count: Number of SMILES to generate

    Returns:
        List of test SMILES strings
    """
    base_smiles = [
        "CCO",  # ethanol
        "CCC",  # propane
        "CCCO",  # propanol
        "CCCC",  # butane
        "CCCCO",  # butanol
        "CC(C)O",  # isopropanol
        "CC(C)C",  # isobutane
        "C1CCCCC1",  # cyclohexane
        "c1ccccc1",  # benzene
        "CCN",  # ethylamine
    ]

    result = []
    for i in range(count):
        if i < len(base_smiles):
            result.append(base_smiles[i])
        else:
            # Generate longer alkanes
            chain_length = (i % 10) + 1
            result.append("C" * chain_length)

    return result

def generate_test_labels(count: int = 10, label_type: str = "binary") -> list:
    """
    Generate test labels.

    Args:
        count: Number of labels to generate
        label_type: Type of labels ("binary", "multiclass", "regression")

    Returns:
        List of test labels
    """
    if label_type == "binary":
        return [i % 2 for i in range(count)]
    elif label_type == "multiclass":
        return [i % 3 for i in range(count)]
    elif label_type == "regression":
        return [float(i) / count for i in range(count)]
    else:
        raise ValueError(f"Unknown label type: {label_type}")

def create_test_dataset_file(count: int = 20, label_type: str = "binary", file_format: str = "csv") -> str:
    """
    Create a complete test dataset file.

    Args:
        count: Number of samples
        label_type: Type of labels
        file_format: File format ("csv" or "sdf")

    Returns:
        Path to the created file
    """
    smiles = generate_test_smiles(count)
    labels = generate_test_labels(count, label_type)

    if file_format == "csv":
        data_rows = []
        for i in range(count):
            smile = smiles[i % len(smiles)]
            label = labels[i % len(labels)]
            data_rows.append([smile, label])

        return create_test_csv_file(data_rows)

    elif file_format == "sdf":
        # For SDF, we'll create a simple format
        molecules = smiles[:count]
        return create_test_sdf_file(molecules)

    else:
        raise ValueError(f"Unsupported file format: {file_format}")

class TestDataManager:
    """
    Manager for test data files and cleanup.
    """

    def __init__(self):
        self.temp_files = []

    def create_csv_file(self, data_rows: list, headers: list = None) -> str:
        """Create CSV file and track for cleanup."""
        file_path = create_test_csv_file(data_rows, headers)
        self.temp_files.append(file_path)
        return file_path

    def create_sdf_file(self, molecules: list) -> str:
        """Create SDF file and track for cleanup."""
        file_path = create_test_sdf_file(molecules)
        self.temp_files.append(file_path)
        return file_path

    def create_dataset_file(self, count: int = 20, label_type: str = "binary", file_format: str = "csv") -> str:
        """Create dataset file and track for cleanup."""
        file_path = create_test_dataset_file(count, label_type, file_format)
        self.temp_files.append(file_path)
        return file_path

    def create_settings_file(self, **kwargs) -> str:
        """Create settings file and track for cleanup."""
        file_path = create_test_settings_file(**kwargs)
        self.temp_files.append(file_path)
        return file_path

    def cleanup_all(self):
        """Clean up all tracked files."""
        for file_path in self.temp_files:
            cleanup_temp_file(file_path)
        self.temp_files = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup_all()

def skip_if_server_unavailable(func):
    """
    Decorator to skip tests if server is not available.
    """
    import functools

    import pytest

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_msg = str(e).lower()
            if any(keyword in error_msg for keyword in ["connection", "refused", "timeout", "network", "unavailable"]):
                pytest.skip(f"Server not available: {e}")
            else:
                raise

    return wrapper

def assert_valid_address(address: str, expected_parts: list = None):
    """
    Assert that an address has the expected format.

    Args:
        address: Address to validate
        expected_parts: Expected parts in the address path
    """
    assert isinstance(address, str)
    assert len(address) > 0

    if expected_parts:
        for part in expected_parts:
            assert part in address, f"Expected '{part}' in address '{address}'"

def assert_api_response(response: Dict[str, Any], expected_keys: list = None):
    """
    Assert that an API response has the expected structure.

    Args:
        response: Response to validate
        expected_keys: Expected keys in the response
    """
    assert isinstance(response, dict)

    if expected_keys:
        for key in expected_keys:
            assert key in response, f"Expected key '{key}' in response"
