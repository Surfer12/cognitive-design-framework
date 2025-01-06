# error_handling.mojo
"""
Comprehensive Error Handling Utilities for Mojo
"""

struct MojoError(Exception):
    """Base error for all Mojo-related exceptions."""
    var message: String
    var code: Int

    fn __init__(message: String, code: Int = -1):
        self.message = message
        self.code = code

struct FileSystemError(MojoError):
    """Specific error for file system operations."""
    var path: String

    fn __init__(
        message: String,
        path: String,
        code: Int = -2
    ):
        super(message, code)
        self.path = path


fn safe_operation[T: AnyType](
    operation: fn() -> T,
    error_handler: fn(MojoError) -> T
) -> T:
    """
    Wrap operations with safe error handling.

    Args:
        operation: Primary function to execute
        error_handler: Fallback function if operation fails

    Returns:
        Result of operation or error handler
    """
    try:
        return operation()
    except e:
        return error_handler(
            MojoError(str(e))
        )
