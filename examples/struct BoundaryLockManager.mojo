struct BoundaryLockManager:
    pass

    locked_boundaries: Set[BoundaryId]
    visitor_queue: PriorityQueue[VisitorContext]

    fn attempt_boundary_lock(inout self) -> Bool:

    if boundary in locked_boundaries:

    visitor_queue.push(visitor)
    return False
    locked_boundaries.add(boundary)
    return True
