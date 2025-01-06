# Demo of cognitive bridge functionality
from examples.core import CognitiveBridge


fn demonstrate_bridge():
    """Demonstrates the cognitive bridge functionality."""
    # Create bridge instance
    var bridge = CognitiveBridge()

    # Process valid input
    bridge.process_input("Tell me about your cognitive process")
    print(bridge.get_feedback())

    # Process invalid input
    bridge.process_input("")
    print(bridge.get_feedback())


fn main():
    demonstrate_bridge()
