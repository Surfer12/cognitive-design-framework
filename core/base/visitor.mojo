"""Core visitor pattern implementation"""

from python import Python


struct Visitor:
    var name: String

    fn __init__(inoutself):
        self.name = "base_visitor"

    fn visit_tag_element(inoutself):
        pass
