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
        metadata_dict["creation_time"] = time_module.time()
        metadata_dict["permission_level"] = 0
        self._metadata = metadata_dict

    fn add_metadata(inout self, key: String, value: String) raises:
        """Add metadata to the tag."""
        if not Python.type(self._metadata) is Python.type(Python.dict()):
            self._metadata = Python.dict()
        self._metadata[key] = value

    fn get_metadata(self, key: String) -> String:
        """Get metadata value."""
        try:
            return str(self._metadata.get(key, ""))
        except:
            return ""

    fn get_metadata_dict(self) -> PythonObject:
        """Return the entire metadata dictionary."""
        return self._metadata

    fn to_python_object(self) raises -> PythonObject:
        """Convert TagElement to a PythonObject."""
        var py_dict = Python.dict()
        py_dict["name"] = self.name
        py_dict["content"] = self.content
        py_dict["metadata"] = self._metadata
        return py_dict

    fn accept(self, visitor: PythonObject) raises:
        """Accept a visitor for processing."""
        var py_obj = self.to_python_object()
        visitor.visit(py_obj)
