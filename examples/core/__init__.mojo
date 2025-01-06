# Core module initialization
from utils.vector import DynamicVector


struct Element:
    """Base element interface."""

    fn accept(self, visitor: Visitor) raises -> None:
        pass


struct Visitor:
    """Base visitor interface."""

    fn visit_tag(self, tag: TagElement) raises -> None:
        pass

    fn visit_attribute(self, attr: AttributeElement) raises -> None:
        pass


struct TagElement:
    """Core tag element implementation."""

    var name: String
    var attributes: DynamicVector[AttributeElement]
    var children: DynamicVector[TagElement]

    fn __init__(inout self, name: String):
        self.name = name
        self.attributes = DynamicVector[AttributeElement]()
        self.children = DynamicVector[TagElement]()


struct AttributeElement:
    """Attribute element implementation."""

    var name: String
    var value: String

    fn __init__(inout self, name: String, value: String):
        self.name = name
        self.value = value


# Export type aliases
alias TagInstance = TagElement
alias TagAttribute = AttributeElement
