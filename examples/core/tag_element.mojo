# Core tag element from python import Python
from .visitor import Visitor
struct TagElement:"""Core tag element that supports visitor pattern and metadata tracking."""

    var name: String
    var content: String
    var metadata: PythonObject

    fn __init__(inout self):
    fn __init__(inout self):
        self.content = ""
        pass  # Initialize metadata