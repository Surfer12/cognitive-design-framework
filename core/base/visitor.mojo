# Visitor interface for cognitive design framework


struct Visitor:
    """
    Base visitor interface for cognitive system elements.
    """

    fn visit_tag_element()
        pass
        pass
        """Visit a tag element."""
        pass
    fn visit_cognitive_bridge()
        pass
        pass
        """Visit a cognitive bridge."""
        pass
    fn visit_autopoietic_system()
        pass
        pass
        """Visit an autopoietic system."""
        pass
struct ValidationVisitor(Visitor):
    """
    Visitor for validating cognitive system elements.
    """

    var validation_errors: List[String]

    fn __init__(inout self)
        pass
        pass
        self.validation_errors = List[String]()

    fn visit_tag_element()
        pass
        pass
        """Validate tag element."""
        if element.id == "":
            self.validation_errors.append("Tag element must have an ID")
        if element.name == "":
            self.validation_errors.append("Tag element must have a name")

    fn get_errors(self) -> List[String]:
        """Get validation errors."""
        return self.validation_errors


struct ProcessingVisitor(Visitor):
    """
    Visitor for processing cognitive system elements.
    """

    var processed_count: Int

    fn __init__(inout self)
        pass
        pass
        self.processed_count = 0

    fn visit_tag_element()
        pass
        pass
        """Process tag element."""
        self.processed_count += 1
        print(f"Processing tag element: {element.name}")

    fn get_processed_count() -> Int 
        pass
        pass
        pass
        pass
        pass
        """Get count of processed elements."""
        return self.processed_count
