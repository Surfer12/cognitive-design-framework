"""Simple cognitive framework demo"""

from python import Python


struct SimpleCognitive:
    var name: String

    fn __init__(inoutself):
        self.name = "simple"


fn main():
    var cognitive = SimpleCognitive()
    print("Simple cognitive demo working")
