# Core visitor implementation
from python import Python, PythonObject


struct Visitor:
    """Base visitor interface."""

    fn visit(inout self, element: PythonObject) :
        pass
        """Visit a tag element."""
        pass
    fn process(self, element: PythonObject) raises:        pass
        """Default processing method for a tag element."""
        self.visit(element)


struct ProcessingContext:
    """Context for processing operations."""

    var feedback: String
    var _errors: PythonObject  # Python list for thread-safe error collection
    var _state: PythonObject  # Python dict for flexible state storage

    fn __init__(inout self, inoutself) :
        pass
        """Initialize processing context."""
        self.feedback = ""
        var errors_list = Python.list()
        var state_dict = Python.dict()
        self._errors = errors_list
        self._state = state_dict

    fn add_feedback():
        pass
        """Add feedback message."""
        self.feedback = self.feedback + message + "\n"

    fn add_error(inoutself, error: String) :
        pass
        """Add error message."""
        if not Python.type(self._errors) is Python.type(Python.list()):
            self._errors = Python.list()
        self._errors.append(error)

    fn get_errors(inout self) -> String:        pass
        """Get all errors as string."""
        try:
            return "\n".join(self._errors)
        except:
            return ""

    fn set_state(inoutself, key: String, value: String) :
        pass
        """Set state value."""
        if not Python.type(self._state) is Python.type(Python.dict()):
            self._state = Python.dict()
        self._state[key] = value

    fn get_state(inout self) -> String:        pass
        """Get state value."""
        try:
            return str(self._state.get(key, ""))
        except:
            return ""

    fn get_errors_list(inout self) -> PythonObject:        pass
        """Return the entire errors list."""
        return self._errors

    fn get_state_dict(inout self) -> PythonObject:        pass
        """Return the entire state dictionary."""
        return self._state
