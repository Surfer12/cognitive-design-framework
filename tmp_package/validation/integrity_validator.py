#!/usr/bin/env python3
"""
Integrity Validator

A comprehensive utility for validating file movements and ensuring data integrity
during reorganization, migration, or backup processes.

Key Features:
- Cross-directory file comparison
- Cryptographic hash-based integrity checks
- Detailed movement and modification tracking
"""

import os
import sys
import hashlib
import argparse
import json
from typing import Dict, List, Any

def calculate_file_hash(filepath: str, hash_algorithm: str = 'sha256') -> str:
    """
    Calculate hash of a file using specified algorithm.

    Args:
        filepath (str): Path to the file
        hash_algorithm (str, optional): Hash algorithm to use. Defaults to 'sha256'.

    Returns:
        str: Hexadecimal hash of the file
    """
    try:
        hasher = hashlib.new(hash_algorithm)
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except (IOError, OSError) as e:
        print(f"Error hashing file {filepath}: {e}")
        return ''

class FileValidator:
    """
    A comprehensive file validation utility for tracking file movements and integrity.
    """

    def __init__(self, original_dir: str, target_dir: str,
                 hash_algorithm: str = 'sha256',
                 ignore_patterns: List[str] = None):
        """
        Initialize FileValidator.

        Args:
            original_dir (str): Source directory path
            target_dir (str): Destination directory path
            hash_algorithm (str, optional): Hash algorithm to use. Defaults to 'sha256'.
            ignore_patterns (List[str], optional): File/directory patterns to ignore
        """
        self.original_dir = os.path.abspath(original_dir)
        self.target_dir = os.path.abspath(target_dir)
        self.hash_algorithm = hash_algorithm
        self.ignore_patterns = ignore_patterns or ['.DS_Store', '.git', '__pycache__']

        self.validation_results: Dict[str, Any] = {
            'total_files': 0,
            'matched_files': 0,
            'mismatched_files': [],
            'missing_files': [],
            'extra_files': []
        }

    def _should_ignore(self, path: str) -> bool:
        """
        Check if a file or directory should be ignored.

        Args:
            path (str): File or directory path

        Returns:
            bool: True if file should be ignored, False otherwise
        """
        return any(pattern in path for pattern in self.ignore_patterns)

    def validate(self) -> Dict[str, Any]:
        """
        Validate files between original and target directories.

        Returns:
            dict: Validation results
        """
        # Track files in target directory to check for extra files
        target_files = set()

        # Walk through original directory
        for root, _, files in os.walk(self.original_dir):
            for filename in files:
                original_path = os.path.join(root, filename)

                # Skip ignored files
                if self._should_ignore(original_path):
                    continue

                # Calculate relative path
                relative_path = os.path.relpath(original_path, self.original_dir)
                target_path = os.path.join(self.target_dir, relative_path)

                self.validation_results['total_files'] += 1
                target_files.add(target_path)

                # Check if file exists in target location
                if not os.path.exists(target_path):
                    self.validation_results['missing_files'].append(relative_path)
                    continue

                # Compare file hashes
                original_hash = calculate_file_hash(original_path, self.hash_algorithm)
                target_hash = calculate_file_hash(target_path, self.hash_algorithm)

                if original_hash == target_hash:
                    self.validation_results['matched_files'] += 1
                else:
                    self.validation_results['mismatched_files'].append(relative_path)

        # Check for extra files in target directory
        for root, _, files in os.walk(self.target_dir):
            for filename in files:
                target_path = os.path.join(root, filename)

                # Skip ignored files
                if self._should_ignore(target_path):
                    continue

                relative_path = os.path.relpath(target_path, self.target_dir)
                original_path = os.path.join(self.original_dir, relative_path)

                if target_path not in target_files and not os.path.exists(original_path):
                    self.validation_results['extra_files'].append(relative_path)

        return self.validation_results

    def generate_report(self, output_format: str = 'text') -> str:
        """
        Generate a validation report.

        Args:
            output_format (str, optional): Report format. Defaults to 'text'.

        Returns:
            str: Formatted validation report
        """
        if output_format == 'json':
            return json.dumps(self.validation_results, indent=2)

        # Default text format
        report = [
            "File Validation Report",
            "=====================",
            f"Total Files: {self.validation_results['total_files']}",
            f"Matched Files: {self.validation_results['matched_files']}",
            f"Missing Files: {len(self.validation_results['missing_files'])}",
            f"Mismatched Files: {len(self.validation_results['mismatched_files'])}",
            f"Extra Files: {len(self.validation_results['extra_files'])}",
            "",
            "Details:",
            "--------"
        ]

        if self.validation_results['missing_files']:
            report.append("Missing Files:")
            report.extend(self.validation_results['missing_files'])

        if self.validation_results['mismatched_files']:
            report.append("\nMismatched Files:")
            report.extend(self.validation_results['mismatched_files'])

        if self.validation_results['extra_files']:
            report.append("\nExtra Files:")
            report.extend(self.validation_results['extra_files'])

        return '\n'.join(report)

def main():
    """
    Command-line interface for file validation.
    """
    parser = argparse.ArgumentParser(description='Validate file movements and integrity.')
    parser.add_argument('original_dir', help='Path to the original directory')
    parser.add_argument('target_dir', help='Path to the target directory')
    parser.add_argument('--hash', default='sha256', help='Hash algorithm to use')
    parser.add_argument('--format', choices=['text', 'json'], default='text',
                        help='Output report format')
    parser.add_argument('--ignore', nargs='+',
                        help='Additional patterns to ignore')

    args = parser.parse_args()

    # Create validator
    validator = FileValidator(
        args.original_dir,
        args.target_dir,
        hash_algorithm=args.hash,
        ignore_patterns=args.ignore
    )

    # Validate and generate report
    validator.validate()
    print(validator.generate_report(args.format))

if __name__ == '__main__':
    main()
