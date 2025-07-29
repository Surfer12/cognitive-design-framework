"""Source core tag element"""

from python import Python


struct TagElement:
    var name: String
    var content: String

    fn __init__(inoutself):
        self.name = ""
        self.content = ""
