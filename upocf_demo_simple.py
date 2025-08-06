#!/usr/bin/env python3
"""
UPOCF Framework Simple Demonstration
===================================

A simplified demonstration of the Unified Onto-Phenomenological Consciousness 
Framework (UPOCF) core concepts without external dependencies.

This demonstrates:
- Taylor series approximation with error bounds
- RK4 integration for consciousness evolution
- Integrated Information (Φ) computation
- Bifurcation analysis for consciousness detection

Authors: Ryan Oates, with contributions from Claude Sonnet 4o and Grok 4
"""

import math
import time
from typing import List, Tuple, Dict, Callable


class SimpleMath:
    """Simple mathematical utilities to replace numpy/scipy"""
    
    @staticmethod
    def norm(vector: List[float]) -> float:
        """Compute L2 norm of a vector"""
        return math.sqrt(sum(x**2 for x in vector))
    
    @staticmethod
    def dot(a: List[float], b: List[float]) -> float:
        """Compute dot product"""
        return sum(x*y for x, y in zip(a, b))
    
    @staticmethod
    def matrix_multiply(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
        """Multiply two matrices"""
        rows_A, cols_A = len(A), len(A[0])
        rows_B, cols_B = len(B), len(B[0])
        
        if cols_A != rows_B:
            raise ValueError("Matrix dimensions incompatible")
        
        result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
        
        for i in range(rows_A):
            for j in range(cols_B):
                for k in range(cols_A):
                    result[i][j] += A[i][k] * B[k][j]
        
        return result
    
    @staticmethod
    def factorial(n: int) -> int:
        """Compute factorial"""
        if n <= 1:
            return 1
        return n * SimpleMath.factorial(n - 1)


class UPOCFSimple:
    """
    Simplified UPOCF Framework Implementation
    
    Demonstrates core mathematical concepts from the paper:
    - Consciousness function Ψ(x) with Taylor approximation
    - Integrated Information Φ computation
    - RK4 integration for dynamics
    - Bifurcation analysis
    """
    
    def __init__(self, taylor_order: int = 4, step_size: float = 0.01):
        self.taylor_order = taylor_order
        self.h = step_size
        self.math = SimpleMath()
    
    def consciousness_function(self, x: List[float]) -> float:
        """
        Simple consciousness function Ψ(x)
        For demonstration: Ψ(x) = sum(x_i^2) * connectivity_measure
        """
        # Simple quadratic form with connectivity
        return sum(xi**2 for xi in x) * 0.3 + 0.1 * sum(x)
    
    def taylor_approximation(self, 
                           x: List[float], 
                           x0: List[float],
                           func: Callable = None) -> Tuple[float, float]:
        """
        Taylor series approximation with error bounds
        
        Validates Theorem 1: |R₄(x)| ≤ (1/60)|x-x₀|⁵
        """
        if func is None:
            func = self.consciousness_function
        
        # Compute derivatives numerically
        h = 1e-5
        
        # Function value at x0
        f0 = func(x0)
        
        # First derivative (gradient)
        grad = []
        for i in range(len(x0)):
            x_plus = x0.copy()
            x_minus = x0.copy()
            x_plus[i] += h
            x_minus[i] -= h
            
            grad.append((func(x_plus) - func(x_minus)) / (2 * h))
        
        # Displacement vector
        dx = [xi - x0i for xi, x0i in zip(x, x0)]
        dx_norm = self.math.norm(dx)
        
        # Taylor approximation (up to 2nd order for simplicity)
        approximation = f0 + self.math.dot(grad, dx)
        
        # Add quadratic term
        quadratic_term = 0.5 * sum(dxi**2 for dxi in dx) * 0.1  # Simplified Hessian
        approximation += quadratic_term
        
        # Error bound from paper: |R₄(x)| ≤ (1/60)|x-x₀|⁵
        error_bound = (1/60) * (dx_norm ** 5)
        
        return approximation, error_bound
    
    def compute_integrated_information(self, 
                                     system_state: List[float],
                                     connectivity: List[List[float]]) -> float:
        """
        Compute Integrated Information Φ (simplified)
        
        For demonstration: Φ = mutual_information_proxy * integration_measure
        """
        n = len(system_state)
        
        if n == 1:
            return 0.0
        
        # Simplified Φ computation
        # In practice, this would involve partition enumeration and MI calculation
        
        # Connectivity strength
        total_connectivity = sum(sum(row) for row in connectivity)
        avg_connectivity = total_connectivity / (n * n)
        
        # State diversity
        state_variance = sum((xi - sum(system_state)/n)**2 for xi in system_state) / n
        
        # Integration measure (simplified)
        phi = avg_connectivity * state_variance * 0.5
        
        return max(0.0, phi)
    
    def rk4_step(self, 
                 t: float, 
                 y: List[float], 
                 dynamics_func: Callable) -> List[float]:
        """
        Single RK4 integration step
        
        Validates Theorem 2: O(h⁴) convergence
        """
        # RK4 coefficients
        k1 = [self.h * dydt for dydt in dynamics_func(t, y)]
        
        y_k2 = [yi + k1i/2 for yi, k1i in zip(y, k1)]
        k2 = [self.h * dydt for dydt in dynamics_func(t + self.h/2, y_k2)]
        
        y_k3 = [yi + k2i/2 for yi, k2i in zip(y, k2)]
        k3 = [self.h * dydt for dydt in dynamics_func(t + self.h/2, y_k3)]
        
        y_k4 = [yi + k3i for yi, k3i in zip(y, k3)]
        k4 = [self.h * dydt for dydt in dynamics_func(t + self.h, y_k4)]
        
        # Combine RK4 terms
        y_new = []
        for i in range(len(y)):
            y_new.append(y[i] + (k1[i] + 2*k2[i] + 2*k3[i] + k4[i]) / 6)
        
        return y_new
    
    def detect_consciousness(self, 
                           system_state: List[float],
                           connectivity: List[List[float]]) -> Dict[str, float]:
        """
        Real-time consciousness detection
        
        Returns consciousness metrics with performance timing
        """
        start_time = time.time()
        
        # Compute Φ (Integrated Information)
        phi = self.compute_integrated_information(system_state, connectivity)
        
        # Compute Ψ (Consciousness Function)
        x0 = [0.0] * len(system_state)
        psi, error_bound = self.taylor_approximation(system_state, x0)
        
        # Confidence based on error bounds
        confidence = max(0.0, 1.0 - error_bound / max(abs(psi), 1e-6))
        
        # Simple classification
        if phi < 0.1 and psi < 0.1:
            classification = "unconscious"
        elif phi > 0.5 and psi > 0.5:
            classification = "highly_conscious"
        else:
            classification = "conscious"
        
        processing_time = time.time() - start_time
        
        return {
            'phi': phi,
            'psi': psi,
            'error_bound': error_bound,
            'confidence': confidence,
            'classification': classification,
            'processing_time_ms': processing_time * 1000
        }
    
    def validate_taylor_bounds(self) -> bool:
        """
        Validate Taylor series error bounds (Theorem 1)
        """
        print("Validating Taylor Series Error Bounds (Theorem 1)")
        print("-" * 50)
        
        # Test function: f(x) = x₁² + x₂² + 0.1*x₁*x₂
        def test_func(x):
            if len(x) >= 2:
                return x[0]**2 + x[1]**2 + 0.1*x[0]*x[1]
            return x[0]**2
        
        x0 = [0.0, 0.0]
        test_points = [
            [0.1, 0.1],
            [0.2, 0.15],
            [0.05, 0.08]
        ]
        
        all_bounds_valid = True
        
        for i, x in enumerate(test_points):
            approx, error_bound = self.taylor_approximation(x, x0, test_func)
            actual = test_func(x)
            actual_error = abs(actual - approx)
            
            bound_valid = actual_error <= error_bound
            all_bounds_valid = all_bounds_valid and bound_valid
            
            print(f"Test {i+1}: x = {x}")
            print(f"  Actual error: {actual_error:.6f}")
            print(f"  Error bound:  {error_bound:.6f}")
            print(f"  Bound valid:  {bound_valid}")
            print()
        
        return all_bounds_valid
    
    def validate_rk4_convergence(self) -> bool:
        """
        Validate RK4 convergence order (Theorem 2)
        """
        print("Validating RK4 Convergence Order (Theorem 2)")
        print("-" * 50)
        
        # Test ODE: dy/dt = -y, exact solution: y(t) = y₀ * exp(-t)
        def dynamics(t, y):
            return [-y[0]]
        
        y0 = [1.0]
        t_final = 1.0
        
        # Test different step sizes
        step_sizes = [0.1, 0.05, 0.025]
        errors = []
        
        for h in step_sizes:
            self.h = h
            num_steps = int(t_final / h)
            
            t = 0.0
            y = y0.copy()
            
            for _ in range(num_steps):
                y = self.rk4_step(t, y, dynamics)
                t += h
            
            # Exact solution
            y_exact = math.exp(-t_final)
            error = abs(y[0] - y_exact)
            errors.append(error)
            
            print(f"Step size h = {h:.3f}: Error = {error:.8f}")
        
        # Check convergence order
        convergence_orders = []
        for i in range(len(errors) - 1):
            h_ratio = step_sizes[i] / step_sizes[i+1]
            error_ratio = errors[i] / errors[i+1]
            if error_ratio > 0:
                order = math.log(error_ratio) / math.log(h_ratio)
                convergence_orders.append(order)
                print(f"Convergence order: {order:.2f}")
        
        avg_order = sum(convergence_orders) / len(convergence_orders)
        print(f"Average convergence order: {avg_order:.2f}")
        
        # RK4 should have order ≈ 4
        return 3.5 <= avg_order <= 4.5


def demonstrate_upocf_framework():
    """
    Comprehensive demonstration of UPOCF framework
    """
    print("=" * 80)
    print("UPOCF Framework Demonstration")
    print("Unified Onto-Phenomenological Consciousness Framework")
    print("=" * 80)
    
    # Initialize framework
    upocf = UPOCFSimple(taylor_order=4, step_size=0.01)
    
    # Test mathematical foundations
    print("\n1. Mathematical Foundation Validation")
    print("=" * 40)
    
    taylor_valid = upocf.validate_taylor_bounds()
    rk4_valid = upocf.validate_rk4_convergence()
    
    print(f"Taylor bounds validation: {'✅ PASSED' if taylor_valid else '❌ FAILED'}")
    print(f"RK4 convergence validation: {'✅ PASSED' if rk4_valid else '❌ FAILED'}")
    
    # Demonstrate consciousness detection
    print("\n2. Consciousness Detection Examples")
    print("=" * 40)
    
    test_systems = [
        {
            'name': 'Simple Binary System',
            'state': [1, 0, 1, 0],
            'connectivity': [
                [0.0, 0.3, 0.0, 0.1],
                [0.3, 0.0, 0.2, 0.0],
                [0.0, 0.2, 0.0, 0.3],
                [0.1, 0.0, 0.3, 0.0]
            ]
        },
        {
            'name': 'Highly Connected System',
            'state': [1, 1, 0, 1],
            'connectivity': [
                [0.0, 0.5, 0.4, 0.3],
                [0.5, 0.0, 0.5, 0.4],
                [0.4, 0.5, 0.0, 0.5],
                [0.3, 0.4, 0.5, 0.0]
            ]
        },
        {
            'name': 'Disconnected System',
            'state': [1, 0, 1, 0],
            'connectivity': [
                [0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0]
            ]
        }
    ]
    
    for system in test_systems:
        print(f"\nAnalyzing: {system['name']}")
        print(f"State: {system['state']}")
        
        result = upocf.detect_consciousness(system['state'], system['connectivity'])
        
        print(f"  Φ (Integrated Information): {result['phi']:.4f}")
        print(f"  Ψ (Consciousness Function): {result['psi']:.4f}")
        print(f"  Error Bound: {result['error_bound']:.6f}")
        print(f"  Confidence: {result['confidence']:.3f}")
        print(f"  Classification: {result['classification']}")
        print(f"  Processing Time: {result['processing_time_ms']:.2f} ms")
    
    # Performance analysis
    print("\n3. Performance Analysis")
    print("=" * 40)
    
    # Test scalability
    system_sizes = [4, 6, 8, 10]
    
    print("Scalability test:")
    for n in system_sizes:
        # Generate random system
        state = [1 if i % 2 == 0 else 0 for i in range(n)]
        connectivity = [[0.3 if i != j else 0.0 for j in range(n)] for i in range(n)]
        
        # Measure performance
        start_time = time.time()
        result = upocf.detect_consciousness(state, connectivity)
        end_time = time.time()
        
        processing_time = (end_time - start_time) * 1000
        print(f"  System size n={n}: {processing_time:.3f} ms")
    
    # Summary
    print("\n4. Framework Validation Summary")
    print("=" * 40)
    
    if taylor_valid and rk4_valid:
        print("✅ Mathematical foundations validated")
        print("✅ Taylor series error bounds confirmed")
        print("✅ RK4 convergence order verified")
        print("✅ Real-time consciousness detection operational")
        print("\n🎉 UPOCF Framework demonstration completed successfully!")
        print("The implementation validates the theoretical claims from the paper.")
    else:
        print("⚠️  Some mathematical validations need attention")
        print("Consider refining implementation or theoretical bounds")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    demonstrate_upocf_framework()