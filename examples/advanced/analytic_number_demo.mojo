"""
Demonstration: Analytic Number Theory in Cognitive Processing
Shows how circle method, sieve theory, and Laurent expansions enhance cognitive reasoning
"""

from systems.consciousness.analytic_number_cognitive import AnalyticNumberCognitive
from collections import List
from math import sin, cos, pi, log, exp

fn generate_cognitive_test_data() -> List[Float64]:
    """Generate test data representing cognitive inputs with various patterns"""
    var data = List[Float64]()
    let N = 200
    
    # Mix of rational and irrational cognitive patterns
    for i in range(N):
        let t = Float64(i) / Float64(N)
        
        # Rational component (major arc behavior)
        let rational_part = sin(2.0 * pi * t * 3.0)  # Period 1/3
        
        # Irrational component (minor arc behavior)  
        let irrational_part = 0.3 * sin(2.0 * pi * t * (2.0 ** 0.5))
        
        # Noise component
        let noise = 0.1 * sin(2.0 * pi * t * 17.0)
        
        # Cognitive complexity measure
        let complexity = rational_part + irrational_part + noise
        data.append(1.0 + 0.5 * complexity)  # Shift to avoid s=1 pole
    
    return data

fn demonstrate_laurent_expansion_insight():
    """Demonstrate how Laurent expansion reveals richer local structure"""
    print("=== Laurent Expansion Analysis ===")
    
    let processor = AnalyticNumberCognitive()
    
    # Test points near cognitive critical point s=1
    let test_points = List[Float64](0.9, 0.95, 0.99, 1.01, 1.05, 1.1)
    
    print("s-value | Zeta(s) | Local Structure Richness")
    print("--------|---------|------------------------")
    
    for s in test_points:
        let zeta_val = processor.cognitive_zeta_function(s)
        let richness = processor._analyze_local_structure(s - 1.0)
        print(f"{s:.2f}    | {zeta_val:.4f}  | {richness:.4f}")
    
    print("\nKey Insight: Local structure richness shows how much the")
    print("regular part (γ + γ₁(s-1) + ...) contributes beyond the singular term 1/(s-1)")

fn demonstrate_circle_method_decomposition():
    """Show how circle method separates rational vs irrational cognitive patterns"""
    print("\n=== Circle Method Decomposition ===")
    
    let processor = AnalyticNumberCognitive()
    let test_data = generate_cognitive_test_data()
    
    var major_arc_count = 0
    var minor_arc_count = 0
    var major_arc_sum = 0.0
    var minor_arc_sum = 0.0
    
    # Analyze first 20 data points for demonstration
    for i in range(min(20, len(test_data))):
        let value = test_data[i]
        let (is_major, contribution) = processor.circle_processor.decompose_cognitive_space(value)
        
        if is_major:
            major_arc_count += 1
            major_arc_sum += contribution
            print(f"Input {i:2d}: {value:.3f} -> MAJOR arc (rational dominance) | contrib: {contribution:.4f}")
        else:
            minor_arc_count += 1
            minor_arc_sum += contribution
            print(f"Input {i:2d}: {value:.3f} -> minor arc (subtle analysis)   | contrib: {contribution:.4f}")
    
    print(f"\nSummary:")
    print(f"Major arcs: {major_arc_count} (avg contrib: {major_arc_sum/max(major_arc_count,1):.4f})")
    print(f"Minor arcs: {minor_arc_count} (avg contrib: {minor_arc_sum/max(minor_arc_count,1):.4f})")

fn demonstrate_sieve_filtering():
    """Show how sieve theory filters and refines cognitive patterns"""
    print("\n=== Sieve Theory Filtering ===")
    
    let processor = AnalyticNumberCognitive()
    let raw_data = generate_cognitive_test_data()
    
    print(f"Original data points: {len(raw_data)}")
    
    # Apply sieve filtering
    let sieve_results = processor.sieve_processor.integrated_sieve_process(raw_data)
    let filtered_data = sieve_results["selberg_filtered"]
    let twin_pairs = sieve_results["brun_twins"]
    let dimension = sieve_results["dimension_estimate"][0]
    
    print(f"After Selberg sieve: {len(filtered_data)} points")
    print(f"Cognitive twin pairs found: {len(twin_pairs)//2}")
    print(f"Estimated cognitive dimension: {dimension:.4f}")
    
    # Show some filtered values
    print("\nFirst 10 filtered values:")
    for i in range(min(10, len(filtered_data))):
        print(f"  {filtered_data[i]:.4f}")

fn demonstrate_integrated_processing():
    """Show complete integrated cognitive processing pipeline"""
    print("\n=== Integrated Cognitive Processing ===")
    
    let processor = AnalyticNumberCognitive()
    let test_data = generate_cognitive_test_data()
    
    # Run complete processing pipeline
    let results = processor.process_cognitive_input(test_data)
    
    print("Processing Results:")
    print(f"  Major arc average:     {results['major_arc_average']:.4f}")
    print(f"  Minor arc average:     {results['minor_arc_average']:.4f}")
    print(f"  Major/minor ratio:     {results['major_minor_ratio']:.4f}")
    print(f"  Cognitive zeta value:  {results['cognitive_zeta']:.4f}")
    print(f"  Local structure rich.: {results['local_structure_richness']:.4f}")
    print(f"  Sieve dimension:       {results['sieve_dimension']:.4f}")
    
    # Detect cognitive gaps
    let gaps = processor.detect_cognitive_gaps(test_data)
    print(f"\nCognitive gaps detected: {len(gaps)}")
    if len(gaps) > 0:
        print("First few gaps:")
        for i in range(min(3, len(gaps))):
            let gap = gaps[i]
            print(f"  Gap {i+1}: [{gap.0:.3f}, {gap.1:.3f}] (size: {gap.1-gap.0:.3f})")

fn demonstrate_cognitive_prime_counting():
    """Show cognitive prime counting function"""
    print("\n=== Cognitive Prime Counting ===")
    
    let processor = AnalyticNumberCognitive()
    
    print("x     | π_cog(x) | x/ln(x) | Ratio")
    print("------|----------|---------|-------")
    
    let test_values = List[Float64](10.0, 50.0, 100.0, 500.0, 1000.0)
    for x in test_values:
        let pi_cog = processor.cognitive_prime_counting(x)
        let asymptotic = x / log(x)
        let ratio = pi_cog / asymptotic
        print(f"{x:5.0f} | {pi_cog:8.2f} | {asymptotic:7.2f} | {ratio:.3f}")

fn main():
    """Run all demonstrations"""
    print("🧠 Analytic Number Theory Cognitive Framework Demo")
    print("=" * 55)
    
    demonstrate_laurent_expansion_insight()
    demonstrate_circle_method_decomposition()
    demonstrate_sieve_filtering()
    demonstrate_integrated_processing()
    demonstrate_cognitive_prime_counting()
    
    print("\n" + "=" * 55)
    print("Demo complete! This framework combines:")
    print("• Circle method: Major/minor arc cognitive decomposition")
    print("• Sieve theory: Pattern filtering and twin detection")  
    print("• Laurent expansion: Rich local structure analysis")
    print("• Integrated processing: Unified cognitive pipeline")
    print("\nThese techniques reveal deep structure in cognitive processes")
    print("that goes beyond simple pattern matching or neural networks.")

if __name__ == "__main__":
    main()
