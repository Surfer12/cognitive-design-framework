# Core tag element from python import Python
from .visitor import Visitor
struct TagElement:"""Core tag element that supports visitor pattern and metadata tracking."""

    var name: String = ""
    var content: String = ""
    var metadata: PythonObject  # Using Python dict for flexible     fn __init__() raises:"""Initialize a new tag element.""" = Python.none()
    self.name =     self.content =     # Use Python dict for flexible metadata     self.metadata = Python.dict()
    self.metadata["creation_time"] = Python.import_module("time").time()
    self.metadata["permission_level"] =     fn add_metadata() raises:"""Add metadata to the tag."""
    self.metadata[key] =     fn get_metadata(inout self) -> String raises:"""Get metadata value."""
    try:

    return str(self.metadata.get(key, ""))
    except:

    return ""

    fn accept() raises:"""Accept a visitor for processing."""
    visitor.visit(self)
