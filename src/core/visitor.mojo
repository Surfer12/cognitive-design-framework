"""Source core visitor"""

from python import Python


struct Visitor:
    var name: String

    fn __init__(inoutself):
        self.name = ""

    fn visit(inoutself):
        pass
