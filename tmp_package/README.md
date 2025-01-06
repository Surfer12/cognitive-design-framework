# Integrity Validator

## Purpose
A flexible Python script for validating file movements, ensuring file integrity during reorganization or migration processes.

## Features
- Compare files between source and target directories
- Calculate file hashes (default: SHA-256)
- Detect:
  - Missing files
  - Mismatched files
  - Extra files
- Support for custom ignore patterns
- Flexible output formats (text/JSON)

## Usage

### Basic Usage
```bash
python integrity_validator.py /path/to/original/dir /path/to/target/dir
```

### Advanced Options
```bash
# Use a different hash algorithm
python integrity_validator.py /original /target --hash md5

# Output in JSON format
python integrity_validator.py /original /target --format json

# Ignore additional file patterns
python integrity_validator.py /original /target --ignore .tmp .cache
```

## Output
- Total number of files
- Matched files count
- Missing files list
- Mismatched files list
- Extra files list

## Installation
Requires Python 3.7+
No additional dependencies beyond standard library

## Customization
- Easily extendable validation logic
- Supports custom hash algorithms
- Flexible reporting options

## License
MIT License
