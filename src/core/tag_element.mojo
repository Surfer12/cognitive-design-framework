# Core tag element implementation
from python import Python, PythonObject

struct TagElement:
    """Core tag element that supports visitor pattern and metadata tracking."""

    var name: String
    var content: String
    var _metadata: PythonObject  # Using Python dict for flexible metadata

    fn __init__(inout self, name: String, content: String) raises:
        """Initialize a new tag element."""
        self.name = name
        self.content = content
        
        # Use Python dict for flexible metadata storage
        var time_module = Python.import_module("time")
        var metadata_dict = Python.dict()
        metadata_dict["creation_time"] = Python.import_module("time").time()
        metadata_dict["permission_level"] = 0
        self.metadata = metadata_dict

    fn add_metadata(inout self, key: String, value: String):
        """Add metadata to the tag."""
        if not isinstance(self.metadata, PythonObject):
            self.metadata = Python.dict()
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
