"""
Simple Demo: Visualization + Storage Integration
Basic example showing matplotlib plots and JSON storage
"""

import sys
from pathlib import Path
import numpy as np

# Add tools to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from tools.visualization.basic_plots import plot_circle_method_simple, plot_laurent_expansion
from tools.storage.simple_storage import SimpleCognitiveStorage

def generate_test_data(n=100):
    """Generate simple test data"""
    return [1.0 + 0.5 * np.sin(2 * np.pi * i / n) for i in range(n)]

def simulate_circle_method(data):
    """Simple circle method simulation"""
    major_arc_indices = []
    minor_arc_indices = []
    
    for i, value in enumerate(data):
        # Simple classification: values close to integers are "major arc"
        if abs(value - round(value)) < 0.2:
            major_arc_indices.append(i)
        else:
            minor_arc_indices.append(i)
    
    return major_arc_indices, minor_arc_indices

def simulate_laurent_analysis():
    """Simple Laurent expansion simulation"""
    s_values = [0.9, 0.95, 0.99, 1.01, 1.05, 1.1]
    zeta_values = []
    
    for s in s_values:
        delta = s - 1.0
        if abs(delta) > 1e-10:
            zeta_val = 1.0 / delta + 0.5772  # Simple Laurent expansion
        else:
            zeta_val = 100.0  # Large value at pole
        zeta_values.append(zeta_val)
    
    return s_values, zeta_values

def main():
    """Run simple demo"""
    print("🧠 Simple Cognitive Analysis Demo")
    print("=" * 40)
    
    # Initialize storage
    storage = SimpleCognitiveStorage()
    
    # Generate and analyze data
    print("1. Generating test data...")
    test_data = generate_test_data(50)
    
    print("2. Running circle method analysis...")
    major_indices, minor_indices = simulate_circle_method(test_data)
    
    print("3. Running Laurent analysis...")
    s_vals, zeta_vals = simulate_laurent_analysis()
    
    # Create visualizations
    print("4. Creating visualizations...")
    plot_circle_method_simple(test_data, major_indices, minor_indices)
    plot_laurent_expansion(s_vals, zeta_vals)
    
    # Save results
    print("5. Saving results...")
    results = {
        "major_arc_count": len(major_indices),
        "minor_arc_count": len(minor_indices),
        "major_minor_ratio": len(major_indices) / max(len(minor_indices), 1),
        "cognitive_zeta_at_1_01": zeta_vals[3],  # s=1.01
        "data_points": len(test_data)
    }
    
    saved_path = storage.save_results(results, "simple_demo")
    
    # Show summary
    print("\n" + "=" * 40)
    print("ANALYSIS COMPLETE")
    print(f"Major arc points: {results['major_arc_count']}")
    print(f"Minor arc points: {results['minor_arc_count']}")
    print(f"Ratio: {results['major_minor_ratio']:.3f}")
    print(f"Cognitive zeta: {results['cognitive_zeta_at_1_01']:.3f}")
    print(f"Results saved to: {saved_path}")

if __name__ == "__main__":
    main()
