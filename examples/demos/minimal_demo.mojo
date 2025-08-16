"""Minimal framework demo"""

from python import Python


struct MinimalBridge:
    var name: String

    fn __init__(inoutself):
        self.name = "Cognitive Bridge"


fn main():
    var bridge = MinimalBridge()
    print("Minimal demo:", bridge.name)
