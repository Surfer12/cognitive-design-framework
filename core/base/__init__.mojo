# Core base components initialization
from python import Python

# Import components
from .tag_element import TagElement
from .visitor import Visitor, ProcessingContext

# Export components
__all__ = ["TagElement", "Visitor", "ProcessingContext"]
