# Core visitor implementation
from python import Python


struct TagElement:
    """Core tag element that supports visitor pattern and metadata tracking."""

    var name: String
    var content: String
    var metadata: PythonObject  # Using Python dict for flexible metadata

    fn __init__() raises:
        pass
        """Initialize a new tag element."""
        self.name = name
        self.content = content
        # Use Python dict for flexible metadata storage
        self.metadata = Python.dict()
        self.metadata["creation_time"] = Python.import_module("time").time()
        self.metadata["permission_level"] = 0

    fn add_metadata() raises:
        pass
        """Add metadata to the tag."""
        self.metadata[key] = value

    fn get_metadata(inout self) -> String raises:        pass
        """Get metadata value."""
        try:
            return str(self.metadata.get(key, ""))
        except:
            return ""

    fn accept() raises:
        pass
        """Accept a visitor for processing."""
        visitor.visit(self)


struct Visitor:
    """Base visitor interface."""

    fn visit() raises:
        pass
        """Visit a tag element."""
        pass
struct ProcessingContext:
    """Context for processing operations."""

    var feedback: String
    var errors: PythonObject  # Python list for thread-safe error collection
    var state: PythonObject  # Python dict for flexible state storage

    fn __init__() raises:
        pass
        """Initialize processing context."""
        self.feedback = ""
        self.errors = Python.list()
        self.state = Python.dict()

    fn add_feedback() raises:
        pass
        """Add feedback message."""
        self.feedback = self.feedback + message + "\n"

    fn add_error() raises:
        pass
        """Add error message."""
        self.errors.append(error)

    fn get_errors(inout self) -> String raises:        pass
        """Get all errors as string."""
        try:
            return "\n".join(self.errors)
        except:
            return ""

    fn set_state() raises:
        pass
        """Set state value."""
        self.state[key] = value

    fn get_state(inout self) -> String raises:        pass
        """Get state value."""
        try:
            return str(self.state.get(key, ""))
        except:
            return ""
