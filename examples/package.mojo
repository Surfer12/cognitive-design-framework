"""
Meta-analysis framework package configuration.

This package provides tools and utilities for performing meta-analysis
of prompts and cognitive processes.
"""

let PACKAGE_NAME = "meta_analysis"
let VERSION = "0.1.0"
let DESCRIPTION = "Framework for meta-analysis of prompts and cognitive processes"
let AUTHOR = "Your Name"

fn get_version() -> String:
    """Return the current package version."""
    return VERSION

fn get_package_info() -> String:
    """Return formatted package information."""
    return f"{PACKAGE_NAME} v{VERSION}\n{DESCRIPTION}" 