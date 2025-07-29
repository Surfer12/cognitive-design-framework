# Core cognitive framework module
from .tag_element import TagElement
from .cognitive_tag_element import CognitiveTagElement
from .visitor import Visitor, ProcessingContext
from .cognitive_bridge import CognitiveBridge

# Export core components
__all__ = [
    "TagElement",
    "CognitiveTagElement",
    "Visitor",
    "ProcessingContext",
    "CognitiveBridge",
]
