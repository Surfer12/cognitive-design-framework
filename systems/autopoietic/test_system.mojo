# Test file for autopoietic from python import Python
from ...core.base.visitor import Visitor, ProcessingContext
from .system import AutopoieticSystem, ConsciousVisitor, SystemState
fn main():# Create an autopoietic system with 0.8 boundary     var system = AutopoieticSystem(0.8)
    pass

    # Add some self-generation     system.add_rule("expand_boundary")
    system.add_rule("increase_complexity")
    system.add_rule("adapt_to_environment")

    # Create a conscious visitor with observation depth 2.5
    var visitor = ConsciousVisitor(2.5)

    # Evolve the     system.evolve()

    # Attempt to visit the     system.accept(visitor)

    # Print     print("Observation insights:")
    for insight in visitor.insights:

    print(" - Depth:", insight["depth"])
    print("   Insight value:", insight["insight_value"])

    # Test system     system.internal_state.set_value("test_key", "test_value")
    print("\nSystem state:")
    print(" - Test value:", system.internal_state.get_value("test_key"))
    print(" - Last rule:", system.internal_state.get_value("last_rule"))
