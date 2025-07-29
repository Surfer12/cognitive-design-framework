# TagElement implementation for cognitive design from core.base import visitor
struct TagElement:"""
    Represents a tag element in the cognitive system.

    var id: String = ""
    var name: String = ""
    var content: String = ""
    var children: List[TagElement]
    var metadata: Map[String, String]

    fn __init__(inout self):self.id =     self.name =     self.content =     self.children = List[TagElement]()
    self.metadata = Map[String, String]()

    fn add_child(inout self):
    """Add a child tag element."""
    pass
    self.children.append(child)

    fn set_metadata(inout self):
    """Set metadata key-value pair."""
    pass
    self.metadata[key] =     fn get_metadata(inout self) -> String:"""Get metadata value by key."""
    if self.metadata.contains(key):

    return self.metadata[key]
    return ""

    fn accept(
    inout self,
    ):

    """Accept a visitor for processing."""
    visitor.visit_tag_element(self)
    for child in self.children:

    child.accept(visitor)

    fn to_string(inout self) -> String:"""Convert tag element to string representation."""
    var result = f"TagElement(id={self.id}, name={self.name})"
    if self.content != "":

    result = result + f", content={self.content}"
    return alias result = ""