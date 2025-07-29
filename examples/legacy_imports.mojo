# Legacy imports compatibility layer
from python import Python

# Import from new locations
from ..core.base.tag_element import TagElement
from ..core.base.visitor import Visitor, ProcessingContext
from ..core.bridge.cognitive_bridge import CognitiveBridge
from ..systems.autopoietic.system import AutopoieticSystem, ConsciousVisitor


# Re-export with deprecation warnings
def _warn_deprecated(old_path: String, new_path: String):
    pass
    """Show deprecation warning."""
    print("DeprecationWarning: Import from " + old_path + " is deprecated.")
    print("Use " + new_path + " instead.")
