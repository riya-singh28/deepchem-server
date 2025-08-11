# Linting Script Usage

The `lint.sh` script provides a convenient way to run code quality checks on Python files using yapf, flake8, and mypy.

## Installation

First, install the required tools:

```bash
pip install yapf flake8 mypy
```

## Usage

```bash
./lint.sh [directory] [options]
```

### Arguments

- `directory` - Directory to lint (default: current directory)

### Options

- `--fix` - Apply yapf formatting automatically
- `--strict` - Use strict mypy checking
- `--help` - Show help message

## Examples

```bash
# Lint current directory
./lint.sh

# Lint specific directory
./lint.sh pyds

# Lint and auto-fix formatting
./lint.sh pyds --fix

# Lint with strict type checking
./lint.sh pyds --strict

# Combine options
./lint.sh pyds --fix --strict
```

## Tools Used

1. **yapf** - Code formatter that follows PEP 8 style guidelines
2. **flake8** - Linter that checks for style and programming errors
3. **mypy** - Static type checker for Python

## Configuration

The script automatically uses configuration from `setup.cfg` if available:

- Looks for `setup.cfg` in the current directory or parent directory
- Uses `[yapf]`, `[flake8]`, and `[mypy]` sections from the configuration file
- Falls back to default configurations if `setup.cfg` is not found

### Setup.cfg Integration

The script will automatically detect and use your project's `setup.cfg` file. For example:

```ini
[yapf]
based_on_style = google
indent_width = 4

[flake8]
max-line-length = 300
ignore = E111,E114,E121,W503,W504

[mypy]
ignore_missing_imports = True
```

### Override Options

- `--strict` option overrides mypy configuration to use strict checking
- `--fix` option applies yapf formatting using the configured style

## Exit Codes

- `0` - All checks passed
- `1` - One or more checks failed or missing dependencies

## Output

The script provides colored output:
- 🔵 Blue: Information messages
- 🟡 Yellow: Warnings
- 🔴 Red: Errors
- 🟢 Green: Success messages
