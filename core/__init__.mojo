# Core module initialization
from python import Python

# Version information
__version__ = "0.1.0"

# Import core components for easy access
from .base.tag_element import TagElement
from .base.visitor import Visitor, ProcessingContext
from .bridge.cognitive_bridge import CognitiveBridge

# Export commonly used components
__all__ = ["TagElement", "Visitor", "ProcessingContext", "CognitiveBridge"]
