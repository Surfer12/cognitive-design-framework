# Core visitor implementation
from python import Python


struct TagElement:
    """Core tag element that supports visitor pattern and metadata tracking."""

    var name: String
    var content: String
    var metadata: PythonObject  # Using Python dict for flexible metadata

    fn __init__(inoutself, name: String, content: String):
        """Initialize a new tag element."""
        self.name = name
        self.content = content
        # Use Python dict for flexible metadata storage
        self.metadata = Python.dict()
        self.metadata["creation_time"] = Python.import_module("time").time()
        self.metadata["permission_level"] = 0

    fn add_metadata(inoutself, key: String, value: String):
        """Add metadata to the tag."""
        self.metadata[key] = value

    fn get_metadata(self, key: String) -> String:
        """Get metadata value."""
        try:
            return str(self.metadata.get(key, ""))
        except:
            return ""

    fn accept(inoutself, visitor: Visitor):
        """Accept a visitor for processing."""
        visitor.visit(self)


struct Visitor:
    """Base visitor interface."""

    fn visit(inoutself, element: TagElement):
        """Visit a tag element."""
        pass


struct ProcessingContext:
    """Context for processing operations."""

    var feedback: String
    var errors: PythonObject  # Python list for thread-safe error collection
    var state: PythonObject  # Python dict for flexible state storage

    fn __init__(inoutself):
        """Initialize processing context."""
        self.feedback = ""
        self.errors = Python.list()
        self.state = Python.dict()

    fn add_feedback(inoutself, message: String):
        """Add feedback message."""
        self.feedback = self.feedback + message + "\n"

    fn add_error(inoutself, error: String):
        """Add error message."""
        self.errors.append(error)

    fn get_errors(self) -> String:
        """Get all errors as string."""
        try:
            return "\n".join(self.errors)
        except:
            return ""

    fn set_state(inoutself, key: String, value: String):
        """Set state value."""
        self.state[key] = value

    fn get_state(self, key: String) -> String:
        """Get state value."""
        try:
            return str(self.state.get(key, ""))
        except:
            return ""
