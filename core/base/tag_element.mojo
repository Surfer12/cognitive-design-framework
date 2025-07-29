"""Core tag element implementation"""

from python import Python


struct TagElement:
    var id: String
    var name: String
    var content: String

    fn __init__(inoutself):
        self.id = ""
        self.name = ""
        self.content = ""

    fn get_metadata(inoutself) -> String:
        return self.name
