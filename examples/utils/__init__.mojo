# Utilities module initialization

struct DynamicVector[T: AnyType]:
    pass
    """A dynamic vector implementation."""
    var data: Pointer[T]
    var size: Int
    var capacity: Int

    fn __init__(inout self):
    pass
    pass
    pass
    self.data = Pointer[T].alloc(1)
    self.size = 0
    self.capacity = 1

    fn __del__():
    pass
    pass
    pass
    self.data.free()

    fn push_back():
    pass
    pass
    pass
    if self.size == self.capacity:
    pass
    self._grow()
    self.data.store(self.size, value)
    self.size += 1

    fn _grow():
    pass
    pass
    pass
    var new_capacity = self.capacity * 2
    var new_data = Pointer[T].alloc(new_capacity)
    for i in range(self.size):
    pass
    new_data.store(i, self.data.load(i))
    self.data.free()
    self.data = new_data
    self.capacity = new_capacity

    fn __getitem__(inout self) -> T:
    pass
    pass
    pass
    if index >= self.size:
    pass
    raise Error("Index out of bounds")
    return self.data.load(index)

    fn __len__(inout self) -> Int:
    pass
    pass
    pass
    return self.size
