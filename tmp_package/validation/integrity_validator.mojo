"""
Integrity Validator in Mojo

A comprehensive utility for validating file movements and ensuring data integrity
during reorganization, migration, or backup processes.

Key Features:
- Cross-directory file comparison
- Cryptographic hash-based integrity checks
- Detailed movement and modification tracking
"""

from python import Python, PythonObject


fn calculate_file_hash(
    filepath: String, hash_algorithm: String = "sha256"
) -> String:
    """
    Calculate hash of a file using specified algorithm.

    Args:
        filepath: Path to the file
        hash_algorithm: Hash algorithm to use. Defaults to 'sha256'.

    Returns:
        Hexadecimal hash of the file
    """
    try:
        # Use Python's hashlib for hash calculation
        var hashlib = Python.import_module("hashlib")
        var os_path = Python.import_module("os.path")
        var open_func = Python.import_module("builtins").open

        # Ensure absolute path
        filepath = os_path.abspath(filepath)

        var hasher = hashlib.new(hash_algorithm)

        with open_func(filepath, "rb") as f:
            while True:
                var chunk = f.read(4096)
                if not chunk:
                    break
                hasher.update(chunk)

        return str(hasher.hexdigest())
    except Exception as e:
        print("Error hashing file " + filepath + ": " + str(e))
        return ""


struct IntegrityValidator:
    """
    A comprehensive file validation utility for tracking file movements and integrity.
    """

    var original_dir: String
    var target_dir: String
    var hash_algorithm: String
    var ignore_patterns: PythonObject
    var validation_results: PythonObject

    fn __init__(
        inout self,
        original_dir: String,
        target_dir: String,
        hash_algorithm: String = "sha256",
        ignore_patterns: PythonObject = None,
    ) raises:
        """
        Initialize IntegrityValidator.

        Args:
            original_dir: Source directory path
            target_dir: Destination directory path
            hash_algorithm: Hash algorithm to use. Defaults to 'sha256'.
            ignore_patterns: File/directory patterns to ignore
        """
        var os_path = Python.import_module("os.path")

        self.original_dir = str(os_path.abspath(original_dir))
        self.target_dir = str(os_path.abspath(target_dir))
        self.hash_algorithm = hash_algorithm

        # Use Python list for ignore patterns
        if ignore_patterns is None:
            self.ignore_patterns = Python.list(
                [".DS_Store", ".git", "__pycache__"]
            )
        else:
            self.ignore_patterns = ignore_patterns

        # Initialize validation results using Python dict
        self.validation_results = Python.dict()
        self.validation_results["total_files"] = 0
        self.validation_results["matched_files"] = 0
        self.validation_results["mismatched_files"] = Python.list()
        self.validation_results["missing_files"] = Python.list()
        self.validation_results["extra_files"] = Python.list()

    fn _should_ignore(self, file_path: String) -> Bool:
        """
        Check if a file or directory should be ignored.

        Args:
            file_path: File or directory path

        Returns:
            True if file should be ignored, False otherwise
        """
        for pattern in self.ignore_patterns:
            if str(pattern) in file_path:
                return True
        return False

    fn validate(inout self) raises -> PythonObject:
        """
        Validate files between original and target directories.

        Returns:
            Validation results dictionary
        """
        var os_walk = Python.import_module("os").walk
        var os_path = Python.import_module("os.path")

        # Track files in target directory to check for extra files
        var target_files = Python.set()

        # Walk through original directory
        for root, _, files in os_walk(self.original_dir):
            for filename in files:
                var original_path = str(os_path.join(str(root), str(filename)))

                # Skip ignored files
                if self._should_ignore(original_path):
                    continue

                # Calculate relative path
                var relative_path = str(
                    os_path.relpath(original_path, self.original_dir)
                )
                var target_path = str(
                    os_path.join(self.target_dir, relative_path)
                )

                self.validation_results["total_files"] += 1
                target_files.add(target_path)

                # Check if file exists in target location
                if not os_path.exists(target_path):
                    self.validation_results["missing_files"].append(
                        relative_path
                    )
                    continue

                # Compare file hashes
                var original_hash = calculate_file_hash(
                    original_path, self.hash_algorithm
                )
                var target_hash = calculate_file_hash(
                    target_path, self.hash_algorithm
                )

                if original_hash == target_hash:
                    self.validation_results["matched_files"] += 1
                else:
                    self.validation_results["mismatched_files"].append(
                        relative_path
                    )

        # Check for extra files in target directory
        for root, _, files in os_walk(self.target_dir):
            for filename in files:
                var target_path = str(os_path.join(str(root), str(filename)))

                # Skip ignored files
                if self._should_ignore(target_path):
                    continue

                var relative_path = str(
                    os_path.relpath(target_path, self.target_dir)
                )
                var original_path = str(
                    os_path.join(self.original_dir, relative_path)
                )

                if target_path not in target_files and not os_path.exists(
                    original_path
                ):
                    self.validation_results["extra_files"].append(relative_path)

        return self.validation_results

    fn generate_report(self, output_format: String = "text") raises -> String:
        """
        Generate a validation report.

        Args:
            output_format: Report format. Defaults to 'text'.

        Returns:
            Formatted validation report
        """
        # Use Python's json module for JSON formatting
        if output_format == "json":
            var json_module = Python.import_module("json")
            return str(json_module.dumps(self.validation_results, indent=2))

        # Default text format
        var report_lines = Python.list()
        report_lines.append("File Validation Report")
        report_lines.append("=====================")
        report_lines.append(
            "Total Files: " + str(self.validation_results["total_files"])
        )
        report_lines.append(
            "Matched Files: " + str(self.validation_results["matched_files"])
        )
        report_lines.append(
            "Missing Files: "
            + str(len(self.validation_results["missing_files"]))
        )
        report_lines.append(
            "Mismatched Files: "
            + str(len(self.validation_results["mismatched_files"]))
        )
        report_lines.append(
            "Extra Files: " + str(len(self.validation_results["extra_files"]))
        )
        report_lines.append("")
        report_lines.append("Details:")
        report_lines.append("--------")

        if len(self.validation_results["missing_files"]) > 0:
            report_lines.append("Missing Files:")
            for file in self.validation_results["missing_files"]:
                report_lines.append(str(file))

        if len(self.validation_results["mismatched_files"]) > 0:
            report_lines.append("\nMismatched Files:")
            for file in self.validation_results["mismatched_files"]:
                report_lines.append(str(file))

        if len(self.validation_results["extra_files"]) > 0:
            report_lines.append("\nExtra Files:")
            for file in self.validation_results["extra_files"]:
                report_lines.append(str(file))

        return "\n".join(report_lines)


fn main() raises:
    """
    Command-line interface for file validation.
    """
    # Use Python's argparse for command-line argument handling
    var argparse = Python.import_module("argparse")
    var parser = argparse.ArgumentParser(
        description="Validate file movements and integrity."
    )
    parser.add_argument("original_dir", help="Path to the original directory")
    parser.add_argument("target_dir", help="Path to the target directory")
    parser.add_argument(
        "--hash", default="sha256", help="Hash algorithm to use"
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output report format",
    )
    parser.add_argument(
        "--ignore", nargs="+", help="Additional patterns to ignore"
    )

    var args = parser.parse_args()

    # Create validator
    var validator = IntegrityValidator(
        str(args.original_dir),
        str(args.target_dir),
        hash_algorithm=str(args.hash),
        ignore_patterns=Python.list(args.ignore) if args.ignore else None,
    )

    # Validate and generate report
    validator.validate()
    print(validator.generate_report(str(args.format)))


# Allow the script to be run directly
fn __main__() raises:
    main()
