# Core visitor implementation
from python import Python
from .tag_element import TagElement


struct Visitor:
    """Base visitor interface."""

    fn visit(inout self, element: TagElement) :
        pass
        """Visit a tag element."""
        pass
struct ProcessingContext:
    """Context for processing operations."""

    var feedback: String
    var errors: PythonObject  # Python list for thread-safe error collection
    var state: PythonObject  # Python dict for flexible state storage

    fn __init__(inout self):
        pass
        """Initialize processing context."""
        self.feedback = ""
        self.errors = Python.list()
        self.state = Python.dict()

    fn add_feedback():
        pass
        """Add feedback message."""
        self.feedback = self.feedback + message + "\n"

    fn add_error():
        pass
        """Add error message."""
        self.errors.append(error)

    fn get_errors(inout self) -> String:        pass
        """Get all errors as string."""
        try:
            return "\n".join(self.errors)
        except:
            return ""

    fn set_state():
        pass
        """Set state value."""
        self.state[key] = value

    fn get_state(inout self) -> String:        pass
        """Get state value."""
        try:
            return str(self.state.get(key, ""))
        except:
            return ""
