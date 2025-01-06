# Core visitor implementation
from python import Python, PythonObject


struct Visitor:
    """Base visitor interface."""

    fn visit(self, element: PythonObject) raises:
        """Visit a tag element."""
        pass

    fn process(self, element: PythonObject) raises:
        """Default processing method for a tag element."""
        self.visit(element)


struct ProcessingContext:
    """Context for processing operations."""

    var feedback: String
    var _errors: PythonObject  # Python list for thread-safe error collection
    var _state: PythonObject  # Python dict for flexible state storage

    fn __init__(inout self) raises:
        """Initialize processing context."""
        self.feedback = ""
        var errors_list = Python.list()
        var state_dict = Python.dict()
        self._errors = errors_list
        self._state = state_dict

    fn add_feedback(inout self, message: String):
        """Add feedback message."""
        self.feedback = self.feedback + message + "\n"

    fn add_error(inout self, error: String) raises:
        """Add error message."""
        if not Python.type(self._errors) is Python.type(Python.list()):
            self._errors = Python.list()
        self._errors.append(error)

    fn get_errors(self) -> String:
        """Get all errors as string."""
        try:
            return "\n".join(self._errors)
        except:
            return ""

    fn set_state(inout self, key: String, value: String) raises:
        """Set state value."""
        if not Python.type(self._state) is Python.type(Python.dict()):
            self._state = Python.dict()
        self._state[key] = value

    fn get_state(self, key: String) -> String:
        """Get state value."""
        try:
            return str(self._state.get(key, ""))
        except:
            return ""

    fn get_errors_list(self) -> PythonObject:
        """Return the entire errors list."""
        return self._errors

    fn get_state_dict(self) -> PythonObject:
        """Return the entire state dictionary."""
        return self._state
