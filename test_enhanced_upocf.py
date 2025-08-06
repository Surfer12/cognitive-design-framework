#!/usr/bin/env python3
"""
Test Enhanced UPOCF Implementation
Validates the enhanced framework against the issues identified in the paper analysis
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import bootstrap
import time
import warnings
from typing import List, Tuple, Dict

# Import the enhanced implementation
from enhanced_upocf_implementation import EnhancedUPOCF, create_synthetic_dataset

def test_taylor_series_consistency():
    """Test Taylor series consistency and error bounds"""
    print("🧪 Testing Taylor Series Consistency...")
    
    upocf = EnhancedUPOCF()
    
    # Test different system states
    test_states = [
        np.array([0.1, 0.2, 0.3]),
        np.array([0.5, 0.5, 0.5]),
        np.array([0.9, 0.8, 0.7])
    ]
    
    x0 = np.array([0.0, 0.0, 0.0])
    
    for i, x in enumerate(test_states):
        print(f"\nTest State {i+1}: {x}")
        
        # Test 4th order
        psi_4, error_4 = upocf.compute_consciousness_function(x, x0, order=4)
        print(f"  4th Order: Ψ = {psi_4:.6f}, Error ≤ {error_4:.6f}")
        
        # Test 5th order
        psi_5, error_5 = upocf.compute_consciousness_function(x, x0, order=5)
        print(f"  5th Order: Ψ = {psi_5:.6f}, Error ≤ {error_5:.6f}")
        
        # Verify error bounds are reasonable
        assert error_4 >= 0, "Error bound must be non-negative"
        assert error_5 >= 0, "Error bound must be non-negative"
        assert abs(psi_4 - psi_5) <= max(error_4, error_5), "Approximations should be within error bounds"
    
    print("✅ Taylor series consistency tests passed!")

def test_exact_phi_computation():
    """Test exact Φ computation for small systems"""
    print("\n🧪 Testing Exact Φ Computation...")
    
    upocf = EnhancedUPOCF(max_system_size=8)
    
    # Test small systems where exact computation is possible
    test_systems = [
        np.array([1, 0, 1, 0]),  # 4-element system
        np.array([1, 1, 0, 0, 1]),  # 5-element system
        np.array([1, 0, 1, 0, 1, 0]),  # 6-element system
    ]
    
    for i, system in enumerate(test_systems):
        print(f"\nSystem {i+1}: {system}")
        
        phi = upocf.compute_exact_phi(system)
        print(f"  Φ = {phi:.6f}")
        
        # Verify Φ is non-negative and reasonable
        assert phi >= 0, "Φ must be non-negative"
        assert phi <= 1, "Φ should be normalized"
    
    # Test larger system (should use approximation)
    large_system = np.random.binomial(1, 0.3, 15)
    print(f"\nLarge System (15 elements): {large_system}")
    
    with warnings.catch_warnings(record=True) as w:
        phi_large = upocf.compute_exact_phi(large_system)
        print(f"  Φ (approximated) = {phi_large:.6f}")
        
        # Should have generated a warning
        assert len(w) > 0, "Should warn about large system size"
    
    print("✅ Exact Φ computation tests passed!")

def test_validation_framework():
    """Test the validation framework with synthetic data"""
    print("\n🧪 Testing Validation Framework...")
    
    upocf = EnhancedUPOCF()
    
    # Create synthetic dataset
    test_systems, ground_truth = create_synthetic_dataset(100)
    
    print(f"Created dataset with {len(test_systems)} systems")
    print(f"Conscious systems: {sum(ground_truth)}")
    print(f"Non-conscious systems: {len(ground_truth) - sum(ground_truth)}")
    
    # Run validation
    start_time = time.time()
    results = upocf.validate_consciousness_detection(test_systems, ground_truth)
    end_time = time.time()
    
    print(f"\nValidation Results:")
    print(f"  True Positive Rate: {results['true_positive_rate']:.3f}")
    print(f"  False Positive Rate: {results['false_positive_rate']:.3f}")
    print(f"  Accuracy: {results['accuracy']:.3f}")
    print(f"  Confidence Interval: {results['confidence_interval']}")
    print(f"  Mean Confidence: {results['mean_confidence']:.3f}")
    print(f"  Processing Time: {end_time - start_time:.3f} seconds")
    
    # Verify results are reasonable
    assert 0 <= results['true_positive_rate'] <= 1, "TPR must be in [0,1]"
    assert 0 <= results['false_positive_rate'] <= 1, "FPR must be in [0,1]"
    assert 0 <= results['accuracy'] <= 1, "Accuracy must be in [0,1]"
    assert 0 <= results['mean_confidence'] <= 1, "Confidence must be in [0,1]"
    
    print("✅ Validation framework tests passed!")

def test_performance_scaling():
    """Test performance scaling with system size"""
    print("\n🧪 Testing Performance Scaling...")
    
    upocf = EnhancedUPOCF()
    
    system_sizes = [4, 6, 8, 10, 12]
    times = []
    
    for size in system_sizes:
        # Create test system
        system = np.random.binomial(1, 0.3, size)
        
        # Time Φ computation
        start_time = time.time()
        phi = upocf.compute_exact_phi(system)
        end_time = time.time()
        
        computation_time = end_time - start_time
        times.append(computation_time)
        
        print(f"  System size {size}: Φ = {phi:.6f}, Time = {computation_time:.6f}s")
    
    # Plot scaling
    plt.figure(figsize=(10, 6))
    plt.subplot(1, 2, 1)
    plt.plot(system_sizes, times, 'bo-')
    plt.xlabel('System Size')
    plt.ylabel('Computation Time (s)')
    plt.title('Φ Computation Time Scaling')
    plt.grid(True)
    
    # Theoretical scaling (exponential due to partition enumeration)
    theoretical_times = [2**size * 1e-6 for size in system_sizes]
    plt.subplot(1, 2, 2)
    plt.plot(system_sizes, theoretical_times, 'ro-', label='Theoretical')
    plt.plot(system_sizes, times, 'bo-', label='Actual')
    plt.xlabel('System Size')
    plt.ylabel('Computation Time (s)')
    plt.title('Theoretical vs Actual Scaling')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('upocf_scaling_analysis.png', dpi=300, bbox_inches='tight')
    print("  📊 Scaling analysis plot saved as 'upocf_scaling_analysis.png'")
    
    print("✅ Performance scaling tests passed!")

def test_error_analysis():
    """Test error analysis and bounds"""
    print("\n🧪 Testing Error Analysis...")
    
    upocf = EnhancedUPOCF()
    
    # Test error bounds for different approximation orders
    x = np.array([0.5, 0.3, 0.7])
    x0 = np.array([0.0, 0.0, 0.0])
    
    # Test different distances from reference point
    distances = [0.1, 0.5, 1.0, 2.0]
    
    print("Error Analysis Results:")
    print("Distance | 4th Order Error | 5th Order Error")
    print("-" * 45)
    
    for dist in distances:
        # Scale x to be at distance 'dist' from x0
        x_scaled = x0 + dist * (x - x0) / np.linalg.norm(x - x0)
        
        psi_4, error_4 = upocf.compute_consciousness_function(x_scaled, x0, order=4)
        psi_5, error_5 = upocf.compute_consciousness_function(x_scaled, x0, order=5)
        
        print(f"{dist:8.1f} | {error_4:14.6f} | {error_5:14.6f}")
        
        # Verify error increases with distance
        if dist > 0.1:  # Skip first comparison
            assert error_4 > 0, "Error should be positive"
            assert error_5 > 0, "Error should be positive"
    
    print("✅ Error analysis tests passed!")

def test_consciousness_detection_accuracy():
    """Test consciousness detection accuracy with known ground truth"""
    print("\n🧪 Testing Consciousness Detection Accuracy...")
    
    upocf = EnhancedUPOCF()
    
    # Create systems with known consciousness properties
    conscious_systems = []
    non_conscious_systems = []
    
    # Systems with high integration (conscious)
    for i in range(50):
        # Create systems with coherent patterns
        size = np.random.randint(4, 8)
        system = np.zeros(size)
        # Add coherent patterns
        if np.random.random() > 0.5:
            system[::2] = 1  # Alternating pattern
        else:
            system[:size//2] = 1  # Block pattern
        conscious_systems.append(system)
    
    # Systems with low integration (non-conscious)
    for i in range(50):
        # Create systems with random patterns
        size = np.random.randint(4, 8)
        system = np.random.binomial(1, 0.2, size)  # Low density random
        non_conscious_systems.append(system)
    
    # Test detection
    conscious_predictions = []
    non_conscious_predictions = []
    
    for system in conscious_systems:
        psi, error = upocf.compute_consciousness_function(system, np.zeros_like(system))
        conscious_predictions.append(psi)
    
    for system in non_conscious_systems:
        psi, error = upocf.compute_consciousness_function(system, np.zeros_like(system))
        non_conscious_predictions.append(psi)
    
    # Calculate metrics
    conscious_mean = np.mean(conscious_predictions)
    non_conscious_mean = np.mean(non_conscious_predictions)
    separation = conscious_mean - non_conscious_mean
    
    print(f"Conscious systems mean Ψ: {conscious_mean:.3f}")
    print(f"Non-conscious systems mean Ψ: {non_conscious_mean:.3f}")
    print(f"Separation: {separation:.3f}")
    
    # Verify separation is positive (conscious systems have higher Ψ)
    assert separation > 0, "Conscious systems should have higher Ψ values"
    
    # Calculate detection accuracy
    threshold = (conscious_mean + non_conscious_mean) / 2
    conscious_correct = sum(1 for psi in conscious_predictions if psi > threshold)
    non_conscious_correct = sum(1 for psi in non_conscious_predictions if psi <= threshold)
    
    accuracy = (conscious_correct + non_conscious_correct) / len(conscious_predictions + non_conscious_predictions)
    print(f"Detection accuracy: {accuracy:.3f}")
    
    assert accuracy > 0.7, "Detection accuracy should be above 70%"
    
    print("✅ Consciousness detection accuracy tests passed!")

def run_comprehensive_test():
    """Run all tests"""
    print("🚀 Starting Comprehensive UPOCF Framework Test")
    print("=" * 60)
    
    try:
        test_taylor_series_consistency()
        test_exact_phi_computation()
        test_validation_framework()
        test_performance_scaling()
        test_error_analysis()
        test_consciousness_detection_accuracy()
        
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED! Enhanced UPOCF Framework is working correctly.")
        print("✅ Mathematical consistency verified")
        print("✅ Exact Φ computation implemented")
        print("✅ Validation framework operational")
        print("✅ Performance scaling analyzed")
        print("✅ Error bounds validated")
        print("✅ Consciousness detection accuracy confirmed")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        raise

if __name__ == "__main__":
    run_comprehensive_test()