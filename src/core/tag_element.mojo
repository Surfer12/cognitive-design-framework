# Core tag element implementation
from python import Python, PythonObject


struct TagElement:
    """Core tag element that supports visitor pattern and metadata tracking."""

    var name: String
    var content: String
    var _metadata: PythonObject  # Using Python dict for flexible metadata

    fn __init__() raises:
        pass
        """Initialize a new tag element."""
        self.name = name
        self.content = content

        # Use Python dict for flexible metadata storage
        var time_module = Python.import_module("time")
        var metadata_dict = Python.dict()
        metadata_dict["creation_time"] = time_module.time()
        metadata_dict["permission_level"] = 0
        self._metadata = metadata_dict

    fn add_metadata() raises:
        pass
        """Add metadata to the tag."""
        if not Python.type(self._metadata) is Python.type(Python.dict()):
            self._metadata = Python.dict()
        self._metadata[key] = value

    fn get_metadata(inout self) -> String raises:        pass
        """Get metadata value."""
        try:
            return str(self._metadata.get(key, ""))
        except:
            return ""

    fn get_metadata_dict(inout self) -> PythonObject raises:        pass
        """Return the entire metadata dictionary."""
        return self._metadata

    fn to_python_object(inout self) -> PythonObject raises:        pass
        """Convert TagElement to a PythonObject."""
        var py_dict = Python.dict()
        py_dict["name"] = self.name
        py_dict["content"] = self.content
        py_dict["metadata"] = self._metadata
        return py_dict

    fn accept() raises:
        pass
        """Accept a visitor for processing."""
        var py_obj = self.to_python_object()
        visitor.visit(py_obj)
