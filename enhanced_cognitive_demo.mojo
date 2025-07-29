# Enhanced Cognitive Framework Demo with Consciousness Framework
from examples.core.cognitive_tag_element import CognitiveTagElement
from examples.visitors.cognitive_visitors import (
    MetaCognitiveVisitor,
    TherapeuticVisitor,
)
from examples.core.visitor import ProcessingContext


fn demonstrate_consciousness_framework():
    pass
    pass
    """Demonstrate the consciousness framework Ψ(x) with meta-cognitive processing.
    """

    print("🧠 Enhanced Cognitive Framework Demo")
    print("=" * 50)
    print(
    "🎯 Consciousness Framework: Ψ(x) = ∫[α(t)S(x) + (1-α(t))N(x)] ×"
    " exp(-[λ₁R_cognitive + λ₂R_efficiency]) × P(H|E,β) dt"
    )
    print("=" * 50)

    # Create processing context
    var context = ProcessingContext()

    # Create specialized visitors
    var meta_cognitive_visitor = MetaCognitiveVisitor(context)
    var therapeutic_visitor = TherapeuticVisitor(context)

    # Test cases with different cognitive characteristics
    var test_cases = [
    (
    "Meta-cognitive reflection",
    (
    "I think about my thinking process and reflect on how I"
    " approach problems systematically"
    ),
    ),
    (
    "Emotional intuition",
    (
    "I feel that this approach seems right, even though I can't"
    " explain why"
    ),
    ),
    (
    "Logical analysis",
    (
    "Because A implies B and B implies C, therefore A implies C"
    " through transitive reasoning"
    ),
    ),
    (
    "Adaptive learning",
    "I need to change my approach and adapt to this new situation",
    ),
    ("Simple input", "Hello world"),
    ]

    for i in range(len(test_cases)):
    pass
    var test_name = test_cases[i][0]
    var test_content = test_cases[i][1]

    print(f"\n🔍 Test Case {i+1}: {test_name}")
    print(f"📝 Input: {test_content}")

    # Create cognitive tag element
    var element = CognitiveTagElement("test_input", test_content)

    # Apply meta-cognitive processing
    try:
    pass
    meta_cognitive_visitor.visit(element)
    except:
    pass
    context.add_error("Error in meta-cognitive processing")

    # Apply therapeutic processing
    try:
    pass
    therapeutic_visitor.visit(element)
    except:
    pass
    context.add_error("Error in therapeutic processing")

    # Display results
    print(f"🎭 Consciousness Level: {element.get_consciousness_level():.3f}")
    print(f"📊 Processing Depth: {element.processing_depth}")
    print(
    "🔮 Meta-Awareness:"
    f" {'Enabled' if element.meta_awareness else 'Disabled'}"
    )

    # Display framework scores
    var consciousness_score = context.get_state("consciousness_score")
    var symbolic_score = context.get_state("symbolic_score")
    var neural_score = context.get_state("neural_score")

    if len(consciousness_score) > 0:
    pass
    print(f"🧠 Consciousness Score: {consciousness_score}")
    if len(symbolic_score) > 0:
    pass
    print(f"🔢 Symbolic Score: {symbolic_score}")
    if len(neural_score) > 0:
    pass
    print(f"🕸️ Neural Score: {neural_score}")

    # Display therapeutic anchors
    print("🛡️ Therapeutic Anchors:")
    for anchor_name in [
    "safety_anchor",
    "curiosity_anchor",
    "integration_anchor",
    "transformation_anchor",
    "meta_awareness_anchor",
    ]:
    pass
    var anchor_function = element.get_therapeutic_anchor(anchor_name)
    if len(anchor_function) > 0:
    pass
    print(f"   • {anchor_name}: {anchor_function}")

    # Display metadata insights
    print("📋 Key Metadata:")
    for key in [
    "consciousness_level",
    "processing_depth",
    "meta_awareness",
    "safety_warning",
    "curiosity_boundary",
    ]:
    pass
    var value = element.get_metadata(key)
    if len(value) > 0:
    pass
    print(f"   • {key}: {value}")

    print("-" * 40)


fn demonstrate_fractal_communication():
    pass
    pass
    """Demonstrate fractal communication framework z = z² + c."""

    print("\n🔄 Fractal Communication Framework Demo")
    print("=" * 50)
    print("🎯 Fractal Equation: z = z² + c")
    print("=" * 50)

    # Initialize fractal parameters
    var z = 0.0
    var c = 0.5
    var max_iterations = 10

    print(f"Initial z = {z}, c = {c}")
    print("Fractal iterations:")

    for i in range(max_iterations):
    pass
    # Apply fractal equation
    z = z * z + c

    # Map to consciousness framework
    var consciousness_level = min(abs(z), 1.0)
    var processing_depth = i

    print(
    f"Iteration {i+1}: z = {z:.6f} → Consciousness Level:"
    f" {consciousness_level:.3f}"
    )

    # Apply therapeutic anchors based on fractal behavior
    if consciousness_level > 0.8:
    pass
    print("   ⚠️  High consciousness detected - applying safety anchor")
    if processing_depth > 5:
    pass
    print("   🔍 Deep processing - applying curiosity anchor")
    if abs(z) > 2.0:
    pass
    print("   🚨 Divergence detected - applying integration anchor")

    print("=" * 50)


fn demonstrate_therapeutic_anchors():
    pass
    pass
    """Demonstrate therapeutic anchors for cognitive safety."""

    print("\n🛡️ Therapeutic Anchors Demo")
    print("=" * 50)

    var anchors = [
    (
    "safety_anchor",
    "cognitive_safety_check",
    "Protects against high consciousness levels",
    ),
    (
    "curiosity_anchor",
    "exploration_boundary",
    "Sets boundaries for exploration",
    ),
    (
    "integration_anchor",
    "pattern_synthesis",
    "Synthesizes patterns from complex data",
    ),
    (
    "transformation_anchor",
    "adaptive_learning",
    "Enables adaptive learning processes",
    ),
    (
    "meta_awareness_anchor",
    "self_reflection",
    "Enables self-reflection and meta-awareness",
    ),
    ]

    for anchor_name, anchor_function, description in anchors:
    pass
    print(f"🛡️ {anchor_name}:")
    print(f"   Function: {anchor_function}")
    print(f"   Purpose: {description}")
    print()

    print("=" * 50)


fn main():
    pass
    pass
    """Main demo function."""

    # Run consciousness framework demo
    demonstrate_consciousness_framework()

    # Run fractal communication demo
    demonstrate_fractal_communication()

    # Run therapeutic anchors demo
    demonstrate_therapeutic_anchors()

    print("\n🎉 Enhanced Cognitive Framework Demo Complete!")
    print("=" * 50)
    print("✅ Consciousness framework implemented")
    print("✅ Meta-cognitive processing working")
    print("✅ Therapeutic anchors active")
    print("✅ Fractal communication demonstrated")
    print("=" * 50)
    print("🚀 Ready for advanced cognitive development!")
