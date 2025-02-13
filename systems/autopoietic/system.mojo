# Autopoietic system implementation
from python import Python
from ...core.base.tag_element import TagElement
from ...core.base.visitor import Visitor, ProcessingContext


struct SystemState:
    """Immutable system state snapshot."""

    var state: PythonObject  # Python dict for thread-safe storage

    fn __init__(inout self):
        self.state = Python.dict()

    fn __init__(inout self, existing_state: PythonObject):
        """Initialize with existing state."""
        self.state = Python.dict(existing_state)  # Create a copy

    fn get_value(self, key: String) -> String:
        """Get state value with optional default."""
        try:
            return str(self.state.get(key, ""))
        except:
            return ""

    fn set_value(inout self, key: String, value: String):
        """Set state value."""
        self.state[key] = value
