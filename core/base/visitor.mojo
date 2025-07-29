# Visitor interface for cognitive design framework


struct Visitor:
    """
    Base visitor interface for cognitive system elements.
    """

    fn visit_tag_element():
        pass
        """Visit a tag element."""
        pass

    fn visit_cognitive_bridge():
        pass
        """Visit a cognitive bridge."""
        pass

    fn visit_autopoietic_system():
        pass
        """Visit an autopoietic system."""
        pass


struct ValidationVisitor:
    """
    Visitor for validating cognitive system elements.
    """

    var validation_errors: List[String]

    fn __init__(inoutself):
        pass
        self.validation_errors = List[String]()

    fn visit_tag_element():
        pass
        """Validate tag element."""
        if element.id == "":
            self.validation_errors.append("Tag element must have an ID")
        if element.name == "":
            self.validation_errors.append("Tag element must have a name")

    fn get_errors(self) -> List[String]:
        """Get validation errors."""
        return self.validation_errors


struct ProcessingVisitor:
    """
    Visitor for processing cognitive system elements.
    """

    var processed_count: Int

    fn __init__(inoutself):
        pass
        self.processed_count = 0

    fn visit_tag_element():
        pass
        """Process tag element."""
        self.processed_count += 1
        print(f"Processing tag element: {element.name}")

    fn get_processed_count(inoutself) -> Int:
        pass
        """Get count of processed elements."""
        return self.processed_count
