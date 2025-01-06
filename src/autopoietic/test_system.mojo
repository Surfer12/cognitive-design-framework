# Test file for autopoietic system
from python import Python
from .system import AutopoieticSystem, ConsciousVisitor, SystemState


fn main() raises:
    # Create an autopoietic system with 0.8 boundary permeability
    var system = AutopoieticSystem(0.8)

    # Add some self-generation rules
    system.add_rule("expand_boundary")
    system.add_rule("increase_complexity")
    system.add_rule("adapt_to_environment")

    # Create a conscious visitor with observation depth 2.5
    var visitor = ConsciousVisitor(2.5)

    # Evolve the system
    system.evolve()

    # Attempt to visit the system
    system.accept(visitor)

    # Print insights
    print("Observation insights:")
    for insight in visitor.insights:
        print(" - Depth:", insight["depth"])
        print("   Insight value:", insight["insight_value"])

    # Test system state
    system.internal_state.set_value("test_key", "test_value")
    print("\nSystem state:")
    print(" - Test value:", system.internal_state.get_value("test_key"))
    print(" - Last rule:", system.internal_state.get_value("last_rule"))
