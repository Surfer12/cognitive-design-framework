"""
Full Visualization Demo
Demonstrates all visualization types: circle method, sieve analysis, and gap detection
"""

import sys
from pathlib import Path
import numpy as np

# Add tools to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from tools.visualization.basic_plots import plot_circle_method_simple, plot_laurent_expansion
from tools.visualization.sieve_plots import (
    plot_sieve_filtering, plot_twin_pairs, plot_prime_patterns, plot_sieve_effectiveness
)
from tools.visualization.gap_plots import (
    plot_cognitive_gaps, plot_gap_statistics, plot_gap_density_analysis, plot_gap_pattern_analysis
)
from tools.storage.simple_storage import SimpleCognitiveStorage

def generate_complex_test_data(n=150):
    """Generate more complex test data with patterns and gaps"""
    data = []
    
    for i in range(n):
        t = i / n
        
        # Multiple frequency components
        base = 1.0 + 0.4 * np.sin(2 * np.pi * t * 2)  # Base pattern
        detail = 0.2 * np.sin(2 * np.pi * t * 7)      # Detail pattern
        noise = 0.1 * np.random.normal()              # Random noise
        
        # Create some gaps by skipping certain ranges
        if 0.3 < t < 0.35 or 0.7 < t < 0.75:
            continue  # Skip these ranges to create gaps
        
        data.append(base + detail + noise)
    
    return data

def simulate_advanced_circle_method(data):
    """More sophisticated circle method simulation"""
    major_arc_indices = []
    minor_arc_indices = []
    
    for i, value in enumerate(data):
        # Check rational approximation quality
        best_rational_dist = float('inf')
        
        # Check approximations with small denominators
        for q in range(1, 11):  # denominators 1-10
            p = round(value * q)
            rational_approx = p / q
            dist = abs(value - rational_approx)
            best_rational_dist = min(best_rational_dist, dist)
        
        # Classify based on rational approximation quality
        if best_rational_dist < 0.15:  # Good rational approximation
            major_arc_indices.append(i)
        else:
            minor_arc_indices.append(i)
    
    return major_arc_indices, minor_arc_indices

def simulate_advanced_sieve(data):
    """Advanced sieve theory simulation"""
    # Selberg sieve: filter out values too close to "composite" patterns
    filtered_data = []
    
    for value in data:
        # Keep values that don't match simple patterns too closely
        keep = True
        
        # Check against small "prime" patterns
        for pattern in [2, 3, 5, 7]:
            scaled_val = value * 10
            if abs(scaled_val % pattern) < 0.5 or abs(scaled_val % pattern - pattern) < 0.5:
                if np.random.random() < 0.3:  # Probabilistic filtering
                    keep = False
                    break
        
        if keep:
            filtered_data.append(value)
    
    # Find twin pairs (values close together)
    twin_pairs = []
    epsilon = 0.08
    
    for i in range(len(filtered_data) - 1):
        if abs(filtered_data[i+1] - filtered_data[i]) < epsilon:
            twin_pairs.append((filtered_data[i], filtered_data[i+1]))
    
    # Cognitive prime patterns
    prime_patterns = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    
    return {
        'original_data': data,
        'filtered_data': filtered_data,
        'twin_pairs': twin_pairs,
        'prime_patterns': prime_patterns
    }

def detect_cognitive_gaps(data, threshold=0.3):
    """Detect gaps in cognitive sequence"""
    if len(data) < 2:
        return []
    
    sorted_data = sorted(data)
    gaps = []
    
    for i in range(len(sorted_data) - 1):
        gap_size = sorted_data[i+1] - sorted_data[i]
        if gap_size > threshold:
            gaps.append((sorted_data[i], sorted_data[i+1]))
    
    return gaps

def main():
    """Run comprehensive visualization demo"""
    print("🧠 Full Cognitive Visualization Demo")
    print("=" * 50)
    
    # Initialize storage
    storage = SimpleCognitiveStorage()
    
    # Generate complex test data
    print("1. Generating complex test data...")
    test_data = generate_complex_test_data(120)
    print(f"   Generated {len(test_data)} data points")
    
    # Circle method analysis
    print("\n2. Circle Method Analysis...")
    major_indices, minor_indices = simulate_advanced_circle_method(test_data)
    print(f"   Major arc: {len(major_indices)} points")
    print(f"   Minor arc: {len(minor_indices)} points")
    
    # Laurent expansion
    print("\n3. Laurent Expansion Analysis...")
    s_vals = [0.8, 0.9, 0.95, 0.99, 1.01, 1.05, 1.1, 1.2]
    zeta_vals = []
    for s in s_vals:
        delta = s - 1.0
        if abs(delta) > 1e-10:
            zeta_val = 1.0 / delta + 0.5772 - 0.0728 * delta
        else:
            zeta_val = 100.0
        zeta_vals.append(zeta_val)
    
    # Sieve analysis
    print("\n4. Sieve Theory Analysis...")
    sieve_results = simulate_advanced_sieve(test_data)
    print(f"   Filtered: {len(sieve_results['filtered_data'])} points")
    print(f"   Twin pairs: {len(sieve_results['twin_pairs'])} pairs")
    
    # Gap detection
    print("\n5. Gap Detection...")
    gaps = detect_cognitive_gaps(sieve_results['filtered_data'], threshold=0.25)
    print(f"   Detected {len(gaps)} cognitive gaps")
    
    # Create all visualizations
    print("\n6. Creating Visualizations...")
    
    print("   - Circle method plots...")
    plot_circle_method_simple(test_data, major_indices, minor_indices)
    plot_laurent_expansion(s_vals, zeta_vals)
    
    print("   - Sieve analysis plots...")
    plot_sieve_filtering(sieve_results['original_data'], sieve_results['filtered_data'])
    plot_twin_pairs(sieve_results['twin_pairs'])
    plot_prime_patterns(sieve_results['prime_patterns'])
    plot_sieve_effectiveness(
        len(sieve_results['original_data']),
        len(sieve_results['filtered_data']),
        len(sieve_results['twin_pairs'])
    )
    
    print("   - Gap analysis plots...")
    plot_cognitive_gaps(sieve_results['filtered_data'], gaps)
    
    if gaps:
        plot_gap_statistics(gaps)
        plot_gap_density_analysis(sieve_results['filtered_data'], gaps, window_size=8)
        if len(gaps) >= 2:
            plot_gap_pattern_analysis(gaps)
    
    # Save comprehensive results
    print("\n7. Saving Results...")
    results = {
        "data_points": len(test_data),
        "major_arc_count": len(major_indices),
        "minor_arc_count": len(minor_indices),
        "major_minor_ratio": len(major_indices) / max(len(minor_indices), 1),
        "cognitive_zeta_at_1_01": zeta_vals[4],  # s=1.01
        "sieve_retention_rate": len(sieve_results['filtered_data']) / len(test_data),
        "twin_pairs_found": len(sieve_results['twin_pairs']),
        "cognitive_gaps": len(gaps),
        "average_gap_size": np.mean([g[1] - g[0] for g in gaps]) if gaps else 0,
        "max_gap_size": max([g[1] - g[0] for g in gaps]) if gaps else 0
    }
    
    saved_path = storage.save_results(results, "full_visual_demo")
    
    # Print comprehensive summary
    print("\n" + "=" * 50)
    print("COMPREHENSIVE ANALYSIS COMPLETE")
    print("=" * 50)
    print(f"Data Points: {results['data_points']}")
    print(f"Major/Minor Ratio: {results['major_minor_ratio']:.3f}")
    print(f"Cognitive Zeta: {results['cognitive_zeta_at_1_01']:.3f}")
    print(f"Sieve Retention: {results['sieve_retention_rate']:.3f}")
    print(f"Twin Pairs: {results['twin_pairs_found']}")
    print(f"Cognitive Gaps: {results['cognitive_gaps']}")
    if results['cognitive_gaps'] > 0:
        print(f"Average Gap Size: {results['average_gap_size']:.3f}")
        print(f"Max Gap Size: {results['max_gap_size']:.3f}")
    print(f"\nResults saved to: {saved_path}")
    
    print("\n🎯 Visualizations Created:")
    print("✅ Circle Method: Major/minor arc classification")
    print("✅ Laurent Expansion: Cognitive zeta function")
    print("✅ Sieve Filtering: Before/after comparison")
    print("✅ Twin Pairs: Brun sieve results")
    print("✅ Prime Patterns: Cognitive prime visualization")
    print("✅ Sieve Effectiveness: Retention and twin rates")
    print("✅ Gap Detection: Sequence gaps highlighted")
    if gaps:
        print("✅ Gap Statistics: Size distribution and analysis")
        print("✅ Gap Density: Spatial gap analysis")
        if len(gaps) >= 2:
            print("✅ Gap Patterns: Spacing and clustering")

if __name__ == "__main__":
    main()
