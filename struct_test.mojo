"""Test struct syntax"""


struct SimpleStruct:
    var name: String

    fn __init__(inoutself, name: String):
        self.name = name


fn main():
    var s = SimpleStruct("test")
    print("Struct test:", s.name)
