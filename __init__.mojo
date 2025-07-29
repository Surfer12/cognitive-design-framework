# Cognitive Design Framework
# Main package initialization

from python import Python

# Version information
__version__ = "0.1.0"
__author__ = "Cognitive Design Framework Team"

# Import core components for easy access
from .core import TagElement, Visitor, ProcessingContext, CognitiveBridge
from .systems import AutopoieticSystem, ConsciousVisitor, SystemState

# Export commonly used components
__all__ = [
    # Core components
    # System components
]

# Package metadata
__metadata__ = {
    "version": __version__,
    "description": (
        "A framework for implementing cognitive processing systems with"
        " autopoietic capabilities"
    ),
    "author": __author__,
    "requires": ["python >= 3.6"],
}
