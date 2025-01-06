# Systems module initialization
from python import Python

# Version information
__version__ = "0.1.0"

# Import system components
from .autopoietic.system import AutopoieticSystem, ConsciousVisitor, SystemState

# Export commonly used components
__all__ = ["AutopoieticSystem", "ConsciousVisitor", "SystemState"]
