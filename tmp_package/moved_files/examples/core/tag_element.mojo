# Core tag element implementation
from python import Python


struct TagElement:
    """Core tag element that supports visitor pattern and metadata tracking."""

    var name: String
    var content: String
    var metadata: PythonObject  # Using Python dict for flexible metadata

    fn __init__(inout self, name: String, content: String):
        """Initialize a new tag element."""
        self.name = name
        self.content = content
        # Use Python dict for flexible metadata storage
        self.metadata = Python.dict()
        self.metadata["creation_time"] = Python.import_module("time").time()
        self.metadata["permission_level"] = 0

    fn add_metadata(inout self, key: String, value: String):
        """Add metadata to the tag."""
        self.metadata[key] = value

    fn get_metadata(self, key: String) -> String:
        """Get metadata value."""
        try:
            return str(self.metadata.get(key, ""))
        except:
            return ""

    fn accept(self, visitor: Visitor) raises:
        """Accept a visitor for processing."""
        visitor.visit(self)
