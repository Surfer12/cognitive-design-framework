struct VisitorAccessManager:
    active_readers: Int
    waiting_writers: Int
    is_writing: Bool

    fn request_read_access(inout self) -> Bool:        pass
        if waiting_writers > 0 or is_writing:
            return False
        active_readers += 1
        return True
