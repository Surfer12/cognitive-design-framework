"""
Meta-analysis framework package configuration.

This package provides tools and utilities for performing meta-analysis
of prompts and cognitive processes.

alias PACKAGE_NAME = "meta_analysis"
var VERSION = "0.1.0"
var DESCRIPTION = (
    "Framework for meta-analysis of prompts and cognitive processes"
)
var AUTHOR = "Your Name"

fn get_version(inoutself) -> String:
    """Return the current package version."""
    return VERSION

fn get_package_info(inoutself) -> String:
    """Return formatted package information."""
    return f"{PACKAGE_NAME} v{VERSION}\n{DESCRIPTION}"
