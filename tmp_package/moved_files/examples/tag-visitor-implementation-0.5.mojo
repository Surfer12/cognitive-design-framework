# Core Element Interface
trait TagElement:
    """Base interface for all visitable elements in our tag system."""
    fn accept(visitor: TagVisitor) raises -> None

# Concrete Elements
struct TagInstance(TagElement):
    """A concrete tag element that can be visited."""
    var name: String
    var attributes: Vector[TagAttribute]
    var children: Vector[TagInstance]
    
    fn accept(self, visitor: TagVisitor) raises -> None:
        """
        The key method that enables the visitor pattern.
        Instead of the element knowing how to process itself,
        it delegates to the visitor.
        """
        visitor.visit_tag(self)
        
        # Recursive visitation of children
        for child in self.children:
            child.accept(visitor)

struct TagAttribute(TagElement):
    """An attribute that can be visited."""
    var name: String
    var value: String
    
    fn accept(self, visitor: TagVisitor) raises -> None:
        visitor.visit_attribute(self)

# Visitor Interface
trait TagVisitor:
    """
    Defines the interface for all operations we might want to perform
    on our tag elements.
    """
    fn visit_tag(tag: TagInstance) raises -> None
    fn visit_attribute(attr: TagAttribute) raises -> None

# Concrete Visitors
struct ValidationVisitor(TagVisitor):
    """
    A visitor that performs validation operations.
    Note how the logic for validation is contained here,
    separate from the tag structure.
    """
    var context: ValidationContext
    
    fn visit_tag(self, tag: TagInstance) raises -> None:
        # Push current tag to context
        self.context.push_tag(tag)
        
        # Perform validation logic specific to tags
        self.validate_tag_structure(tag)
        
        # Context is automatically maintained as we traverse
        self.context.pop_tag()
    
    fn visit_attribute(self, attr: TagAttribute) raises -> None:
        # Validation logic specific to attributes
        self.validate_attribute_value(attr)

struct ParsingVisitor(TagVisitor):
    """
    A different visitor that handles parsing operations.
    Uses the same structure but performs completely different operations.
    """
    var parser_context: ParserContext
    
    fn visit_tag(self, tag: TagInstance) raises -> None:
        # Parsing logic for tags
        self.parser_context.begin_tag(tag)
        # ... parsing operations ...
        self.parser_context.end_tag()
    
    fn visit_attribute(self, attr: TagAttribute) raises -> None:
        # Parsing logic for attributes
        self.parse_attribute_value(attr)

# Usage Example
fn process_tag_structure(root: TagInstance):
    # Create different visitors for different operations
    let validator = ValidationVisitor(ValidationContext())
    let parser = ParsingVisitor(ParserContext())
    
    # The same tag structure can be processed differently
    # by different visitors without changing the tag structure
    root.accept(validator)  # Performs validation
    root.accept(parser)     # Performs parsing
