struct BoundaryLockManager:
    pass
    pass
    locked_boundaries: Set[BoundaryId]
    visitor_queue: PriorityQueue[VisitorContext]

    fn attempt_boundary_lock(inout self) -> Bool:
    pass
    pass
    pass
    if boundary in locked_boundaries:
    pass
    visitor_queue.push(visitor)
    return False
    locked_boundaries.add(boundary)
    return True
