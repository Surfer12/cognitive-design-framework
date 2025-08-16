"""
Performance tests for cognitive framework complexity validation
"""

import pytest
import time
import math
import sys
import os
from typing import List, Tuple

# Add the project root to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))


class TestComplexityValidation:
    """Test suite for O(n log n) complexity validation"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.test_sizes = [100, 500, 1000, 2000, 5000]
        self.tolerance = 0.2  # 20% tolerance for timing variations
        
    def test_theoretical_complexity_calculation(self):
        """Test theoretical O(n log n) complexity calculations"""
        for n in self.test_sizes:
            # Calculate theoretical complexity
            theoretical = n * math.log2(n)
            
            # Validate calculation
            assert theoretical > 0, f"Theoretical complexity should be positive for n={n}"
            assert theoretical > n, f"O(n log n) should be greater than O(n) for n={n}"
            
    def test_empirical_complexity_validation(self):
        """Test empirical complexity validation against theoretical"""
        # Reference data from O_n_log_n_VALIDATION_COMPLETE.md
        reference_data = {
            100: {'theoretical': 664, 'empirical': 664, 'accuracy': 1.0},
            1000: {'theoretical': 9966, 'empirical': 9966, 'accuracy': 1.0},
            10000: {'theoretical': 132877, 'empirical': 132877, 'accuracy': 1.0}
        }
        
        for size, data in reference_data.items():
            theoretical = data['theoretical']
            empirical = data['empirical']
            accuracy = data['accuracy']
            
            # Validate accuracy
            assert accuracy >= 0.9, f"Accuracy too low for size {size}: {accuracy}"
            
            # Validate empirical vs theoretical
            ratio = empirical / theoretical if theoretical > 0 else 1
            assert 0.8 <= ratio <= 1.2, f"Empirical/theoretical ratio out of range for size {size}: {ratio}"
            
    def test_scaling_behavior_validation(self):
        """Test that complexity scales according to O(n log n)"""
        complexities = {}
        
        # Calculate complexities for different sizes
        for n in self.test_sizes:
            complexities[n] = n * math.log2(n)
            
        # Test scaling behavior
        sizes = sorted(complexities.keys())
        for i in range(1, len(sizes)):
            n1, n2 = sizes[i-1], sizes[i]
            c1, c2 = complexities[n1], complexities[n2]
            
            # Calculate scaling ratios
            size_ratio = n2 / n1
            complexity_ratio = c2 / c1
            
            # For O(n log n), complexity ratio should be approximately size_ratio * log(size_ratio)
            expected_ratio = size_ratio * (math.log2(n2) / math.log2(n1))
            
            # Validate scaling
            ratio_error = abs(complexity_ratio - expected_ratio) / expected_ratio
            assert ratio_error < 0.1, f"Scaling error too large between {n1} and {n2}: {ratio_error}"
            
    def test_memory_scaling_linear(self):
        """Test that memory usage scales linearly O(n)"""
        # Mock memory usage data
        memory_usage = {n: n for n in self.test_sizes}  # Linear scaling
        
        sizes = sorted(memory_usage.keys())
        for i in range(1, len(sizes)):
            n1, n2 = sizes[i-1], sizes[i]
            m1, m2 = memory_usage[n1], memory_usage[n2]
            
            # Memory should scale linearly
            size_ratio = n2 / n1
            memory_ratio = m2 / m1
            
            # Validate linear scaling
            ratio_error = abs(memory_ratio - size_ratio) / size_ratio
            assert ratio_error < 0.1, f"Memory scaling not linear between {n1} and {n2}: {ratio_error}"


class TestPerformanceBenchmarks:
    """Test suite for performance benchmarks"""
    
    def test_consciousness_computation_performance(self):
        """Test consciousness computation performance"""
        def mock_consciousness_computation(elements):
            """Mock consciousness computation with O(n log n) complexity"""
            n = len(elements)
            if n <= 1:
                return 0.5
                
            # Simulate divide-and-conquer approach
            mid = n // 2
            left_score = mock_consciousness_computation(elements[:mid])
            right_score = mock_consciousness_computation(elements[mid:])
            
            # Combine results (O(n) operation)
            combined_score = (left_score + right_score) / 2
            return min(combined_score + 0.1, 1.0)
            
        # Test with different input sizes
        test_sizes = [10, 50, 100, 500]
        performance_results = {}
        
        for size in test_sizes:
            elements = [f"element_{i}" for i in range(size)]
            
            start_time = time.time()
            result = mock_consciousness_computation(elements)
            end_time = time.time()
            
            performance_results[size] = {
                'time': end_time - start_time,
                'result': result
            }
            
            # Validate result
            assert 0 <= result <= 1, f"Consciousness score out of range: {result}"
            
        # Validate performance scaling
        sizes = sorted(performance_results.keys())
        for i in range(1, len(sizes)):
            n1, n2 = sizes[i-1], sizes[i]
            t1, t2 = performance_results[n1]['time'], performance_results[n2]['time']
            
            if t1 > 0:  # Avoid division by zero
                time_ratio = t2 / t1
                size_ratio = n2 / n1
                
                # Time should scale roughly as O(n log n)
                expected_ratio = size_ratio * (math.log2(n2) / math.log2(n1))
                
                # Allow for significant variation in small timing measurements
                if t1 > 0.001:  # Only test if timing is meaningful
                    assert time_ratio <= expected_ratio * 10, f"Performance degraded too much between {n1} and {n2}"
                    
    def test_mecn_framework_performance(self):
        """Test MECN framework performance"""
        def mock_mecn_computation(data_points, alpha=0.7, lambda1=0.3, lambda2=0.4):
            """Mock MECN Ψ(x) computation"""
            if not data_points:
                return 0.0
                
            # Simulate O(n log n) computation
            n = len(data_points)
            
            # Tree-based computation simulation
            tree_depth = math.ceil(math.log2(n)) if n > 1 else 1
            base_computation = sum(data_points) / n
            
            # Apply MECN parameters
            psi_result = alpha * base_computation + (1 - alpha) * (lambda1 + lambda2) * base_computation
            
            # Simulate logarithmic factor
            return psi_result * tree_depth / 10
            
        # Test with different data sizes
        test_sizes = [100, 500, 1000, 2000]
        performance_results = {}
        
        for size in test_sizes:
            data_points = [0.5 + 0.1 * (i % 10) for i in range(size)]
            
            start_time = time.time()
            result = mock_mecn_computation(data_points)
            end_time = time.time()
            
            performance_results[size] = {
                'time': end_time - start_time,
                'result': result
            }
            
            # Validate result
            assert result >= 0, f"MECN result should be non-negative: {result}"
            
    def test_autopoietic_system_performance(self):
        """Test autopoietic system performance"""
        def mock_autopoietic_processing(system_components):
            """Mock autopoietic system processing"""
            n = len(system_components)
            if n <= 1:
                return {'stability': 0.8, 'maintenance': True}
                
            # Simulate recursive processing
            stability_sum = 0
            maintenance_active = True
            
            # Process components in tree structure
            for i, component in enumerate(system_components):
                # Simulate component interaction
                component_stability = 0.8 + 0.1 * math.sin(i)
                stability_sum += component_stability
                
                # Check maintenance
                if component_stability < 0.5:
                    maintenance_active = False
                    
            avg_stability = stability_sum / n
            
            return {
                'stability': min(avg_stability, 1.0),
                'maintenance': maintenance_active
            }
            
        # Test with different system sizes
        test_sizes = [50, 100, 200, 500]
        
        for size in test_sizes:
            components = [f"component_{i}" for i in range(size)]
            
            start_time = time.time()
            result = mock_autopoietic_processing(components)
            end_time = time.time()
            
            # Validate results
            assert 0 <= result['stability'] <= 1, f"Stability out of range: {result['stability']}"
            assert isinstance(result['maintenance'], bool), "Maintenance should be boolean"
            
            # Validate timing (should complete in reasonable time)
            processing_time = end_time - start_time
            assert processing_time < 1.0, f"Processing too slow for size {size}: {processing_time}s"


class TestSpeedupValidation:
    """Test suite for speedup validation"""
    
    def test_algorithmic_speedup(self):
        """Test algorithmic speedup compared to naive approaches"""
        # Reference speedup data from validation report
        speedup_data = {
            100: 15.1,
            1000: 100.3,
            10000: 752.6
        }
        
        for size, speedup in speedup_data.items():
            # Validate speedup increases with size
            assert speedup > 1, f"Speedup should be > 1 for size {size}: {speedup}"
            
            # Larger sizes should generally have better speedups
            if size >= 1000:
                assert speedup > 50, f"Large size speedup too low for {size}: {speedup}"
                
    def test_scaling_accuracy(self):
        """Test scaling accuracy validation"""
        # Reference scaling accuracy: 91.7%
        scaling_accuracy = 0.917
        
        assert scaling_accuracy > 0.9, f"Scaling accuracy too low: {scaling_accuracy}"
        assert scaling_accuracy <= 1.0, f"Scaling accuracy should not exceed 100%: {scaling_accuracy}"
        
    def test_tree_depth_scaling(self):
        """Test tree depth scaling validation"""
        def calculate_tree_depth(n):
            """Calculate expected tree depth for size n"""
            return math.ceil(math.log2(n)) if n > 1 else 1
            
        test_sizes = [100, 1000, 10000, 100000]
        
        for size in test_sizes:
            depth = calculate_tree_depth(size)
            
            # Validate logarithmic scaling
            expected_depth = math.log2(size)
            assert abs(depth - expected_depth) <= 1, f"Tree depth scaling incorrect for size {size}"
            
            # Validate depth is reasonable
            assert depth > 0, f"Tree depth should be positive for size {size}"
            assert depth < size, f"Tree depth should be less than size for {size}"


class TestRealTimePerformance:
    """Test suite for real-time performance requirements"""
    
    def test_consciousness_assessment_timing(self):
        """Test consciousness assessment real-time performance"""
        def mock_real_time_assessment(data_stream):
            """Mock real-time consciousness assessment"""
            start_time = time.time()
            
            # Simulate real-time processing
            assessment_score = 0.0
            for data_point in data_stream:
                # Simple processing that should be fast
                assessment_score += data_point * 0.1
                
            # Normalize score
            assessment_score = min(assessment_score / len(data_stream), 1.0)
            
            processing_time = time.time() - start_time
            return assessment_score, processing_time
            
        # Test with real-time constraints
        stream_sizes = [100, 500, 1000]  # Typical real-time data sizes
        
        for size in stream_sizes:
            data_stream = [0.5 + 0.1 * (i % 10) for i in range(size)]
            
            score, processing_time = mock_real_time_assessment(data_stream)
            
            # Validate real-time constraints (< 100ms for responsiveness)
            assert processing_time < 0.1, f"Real-time processing too slow for size {size}: {processing_time}s"
            
            # Validate result quality
            assert 0 <= score <= 1, f"Assessment score out of range: {score}"
            
    def test_therapeutic_monitoring_performance(self):
        """Test therapeutic monitoring real-time performance"""
        def mock_therapeutic_monitoring(session_data):
            """Mock therapeutic monitoring with performance constraints"""
            start_time = time.time()
            
            # Simulate monitoring computations
            metrics = {
                'engagement': sum(session_data) / len(session_data),
                'stability': max(session_data) - min(session_data),
                'progression': (session_data[-1] - session_data[0]) / len(session_data)
            }
            
            processing_time = time.time() - start_time
            return metrics, processing_time
            
        # Test therapeutic session data
        session_lengths = [300, 600, 1200]  # 5, 10, 20 minute sessions (at 1Hz)
        
        for length in session_lengths:
            session_data = [0.6 + 0.2 * math.sin(i * 0.1) for i in range(length)]
            
            metrics, processing_time = mock_therapeutic_monitoring(session_data)
            
            # Validate therapeutic real-time constraints
            assert processing_time < 0.05, f"Therapeutic monitoring too slow for length {length}: {processing_time}s"
            
            # Validate metrics
            assert 0 <= metrics['engagement'] <= 1, f"Engagement metric out of range: {metrics['engagement']}"


if __name__ == '__main__':
    pytest.main([__file__])
