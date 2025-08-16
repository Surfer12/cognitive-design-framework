"""
Simple Demo Without External Dependencies
Basic demonstration of cognitive analysis concepts
"""

import sys
import math
import random
from pathlib import Path

# Add tools to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

def generate_test_data(n=50):
    """Generate simple test data using built-in math"""
    data = []
    for i in range(n):
        t = i / n
        # Simple sine wave with noise
        value = 1.0 + 0.5 * math.sin(2 * math.pi * t * 3) + 0.1 * (random.random() - 0.5)
        data.append(value)
    return data

def simulate_circle_method(data):
    """Simple circle method simulation"""
    major_arc = []
    minor_arc = []
    
    for i, value in enumerate(data):
        # Simple classification: values close to integers are "major arc"
        if abs(value - round(value)) < 0.2:
            major_arc.append(i)
        else:
            minor_arc.append(i)
    
    return major_arc, minor_arc

def simulate_sieve_filtering(data):
    """Simple sieve filtering"""
    filtered = []
    for value in data:
        # Keep values that don't match simple patterns
        if abs(value - 1.0) > 0.1:  # Remove values too close to 1
            filtered.append(value)
    return filtered

def detect_gaps(data, threshold=0.3):
    """Simple gap detection"""
    if len(data) < 2:
        return []
    
    sorted_data = sorted(data)
    gaps = []
    
    for i in range(len(sorted_data) - 1):
        gap_size = sorted_data[i+1] - sorted_data[i]
        if gap_size > threshold:
            gaps.append((sorted_data[i], sorted_data[i+1]))
    
    return gaps

def print_ascii_histogram(data, title, width=50):
    """Print simple ASCII histogram"""
    print(f"\n{title}")
    print("=" * len(title))
    
    if not data:
        print("No data to display")
        return
    
    min_val = min(data)
    max_val = max(data)
    
    if max_val == min_val:
        print("All values are the same")
        return
    
    # Create bins
    n_bins = 10
    bin_width = (max_val - min_val) / n_bins
    bins = [0] * n_bins
    
    # Fill bins
    for value in data:
        bin_idx = min(int((value - min_val) / bin_width), n_bins - 1)
        bins[bin_idx] += 1
    
    # Print histogram
    max_count = max(bins) if bins else 1
    for i, count in enumerate(bins):
        bin_start = min_val + i * bin_width
        bin_end = min_val + (i + 1) * bin_width
        bar_length = int((count / max_count) * width) if max_count > 0 else 0
        bar = "█" * bar_length
        print(f"{bin_start:.2f}-{bin_end:.2f}: {bar} ({count})")

def main():
    """Run simple demo"""
    print("🧠 Simple Cognitive Analysis Demo")
    print("=" * 40)
    
    # Generate test data
    print("1. Generating test data...")
    test_data = generate_test_data(80)
    print(f"   Generated {len(test_data)} data points")
    print(f"   Range: {min(test_data):.3f} to {max(test_data):.3f}")
    
    # Circle method analysis
    print("\n2. Circle Method Analysis...")
    major_indices, minor_indices = simulate_circle_method(test_data)
    major_ratio = len(major_indices) / len(test_data)
    print(f"   Major arc: {len(major_indices)} points ({major_ratio:.1%})")
    print(f"   Minor arc: {len(minor_indices)} points ({1-major_ratio:.1%})")
    
    # Show some examples
    print("   Major arc examples:", [f"{test_data[i]:.3f}" for i in major_indices[:5]])
    print("   Minor arc examples:", [f"{test_data[i]:.3f}" for i in minor_indices[:5]])
    
    # Sieve filtering
    print("\n3. Sieve Analysis...")
    filtered_data = simulate_sieve_filtering(test_data)
    retention_rate = len(filtered_data) / len(test_data)
    print(f"   Original: {len(test_data)} points")
    print(f"   Filtered: {len(filtered_data)} points")
    print(f"   Retention rate: {retention_rate:.1%}")
    
    # Gap detection
    print("\n4. Gap Detection...")
    gaps = detect_gaps(filtered_data, threshold=0.25)
    print(f"   Detected {len(gaps)} cognitive gaps")
    
    if gaps:
        gap_sizes = [end - start for start, end in gaps]
        avg_gap = sum(gap_sizes) / len(gap_sizes)
        max_gap = max(gap_sizes)
        print(f"   Average gap size: {avg_gap:.3f}")
        print(f"   Maximum gap size: {max_gap:.3f}")
        
        print("   Gap details:")
        for i, (start, end) in enumerate(gaps[:5]):  # Show first 5 gaps
            print(f"     Gap {i+1}: [{start:.3f}, {end:.3f}] (size: {end-start:.3f})")
    
    # Laurent expansion simulation
    print("\n5. Laurent Expansion Analysis...")
    s_values = [0.9, 0.95, 0.99, 1.01, 1.05, 1.1]
    print("   s-value | ζ_cog(s) | Local Richness")
    print("   --------|----------|---------------")
    
    for s in s_values:
        delta = s - 1.0
        if abs(delta) > 1e-10:
            singular_part = 1.0 / delta
            regular_part = 0.5772 - 0.0728 * delta  # Euler-Mascheroni + correction
            zeta_val = singular_part + regular_part
            richness = abs(regular_part) / (abs(singular_part) + abs(regular_part))
        else:
            zeta_val = float('inf')
            richness = 1.0
        
        print(f"   {s:6.2f}  | {zeta_val:8.3f} | {richness:13.3f}")
    
    # ASCII visualizations
    print_ascii_histogram(test_data, "Original Data Distribution")
    print_ascii_histogram(filtered_data, "Filtered Data Distribution")
    
    if gaps:
        gap_sizes = [end - start for start, end in gaps]
        print_ascii_histogram(gap_sizes, "Gap Size Distribution")
    
    # Summary
    print("\n" + "=" * 40)
    print("ANALYSIS SUMMARY")
    print("=" * 40)
    print(f"Data Points: {len(test_data)}")
    print(f"Major/Minor Ratio: {len(major_indices)/max(len(minor_indices),1):.3f}")
    print(f"Sieve Retention: {retention_rate:.1%}")
    print(f"Cognitive Gaps: {len(gaps)}")
    
    # Cognitive insights
    print("\n🧠 COGNITIVE INSIGHTS:")
    if major_ratio > 0.6:
        print("• High rational processing dominance")
    elif major_ratio < 0.4:
        print("• High intuitive processing dominance")
    else:
        print("• Balanced rational/intuitive processing")
    
    if retention_rate > 0.8:
        print("• Low cognitive noise (high signal quality)")
    elif retention_rate < 0.5:
        print("• High cognitive noise (needs filtering)")
    else:
        print("• Moderate cognitive noise levels")
    
    if len(gaps) > len(filtered_data) * 0.1:
        print("• Significant cognitive discontinuities detected")
    else:
        print("• Smooth cognitive processing flow")
    
    print("\n✅ Demo complete! This shows how analytic number theory")
    print("   concepts can reveal structure in cognitive processing.")

if __name__ == "__main__":
    main()
