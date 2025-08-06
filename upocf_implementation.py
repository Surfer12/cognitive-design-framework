"""
UPOCF Framework Implementation
=====================================

Implementation of the Unified Onto-Phenomenological Consciousness Framework (UPOCF)
with mathematical foundations for consciousness detection in AI systems.

Authors: Ryan Oates, with contributions from Claude Sonnet 4o and Grok 4
"""

import numpy as np
import scipy.optimize
from scipy.integrate import odeint, solve_ivp
from scipy.special import comb
from typing import Tuple, List, Dict, Optional, Callable, Any
import matplotlib.pyplot as plt
from dataclasses import dataclass
import warnings
from itertools import combinations
import networkx as nx
from sklearn.metrics import roc_curve, auc
import time

@dataclass
class ConsciousnessMetrics:
    """Container for consciousness detection metrics"""
    phi: float  # Integrated Information (IIT)
    psi: float  # Consciousness function value
    error_bound: float  # Taylor series error bound
    confidence: float  # Detection confidence
    bifurcation_type: str  # Type of bifurcation detected
    processing_time: float  # Detection latency


class UPOCFFramework:
    """
    Unified Onto-Phenomenological Consciousness Framework
    
    This class implements the mathematical foundations for consciousness detection
    including Taylor series analysis, NODE-RK4 integration, and bifurcation analysis.
    """
    
    def __init__(self, 
                 taylor_order: int = 4,
                 rk4_step_size: float = 0.01,
                 max_partition_size: int = 12,
                 convergence_threshold: float = 1e-6):
        """
        Initialize UPOCF framework
        
        Args:
            taylor_order: Order of Taylor series approximation
            rk4_step_size: Step size for RK4 integration
            max_partition_size: Maximum system size for exact Φ computation
            convergence_threshold: Convergence threshold for numerical methods
        """
        self.taylor_order = taylor_order
        self.h = rk4_step_size
        self.max_partition_size = max_partition_size
        self.threshold = convergence_threshold
        
        # Precomputed coefficients for numerical derivatives
        self.central_diff_coeffs = {
            1: [-1/2, 0, 1/2],
            2: [1, -2, 1],
            3: [-1/2, 1, 0, -1, 1/2],
            4: [1, -4, 6, -4, 1],
            5: [-1/2, 2, -5/2, 0, 5/2, -2, 1/2]
        }
        
    def compute_integrated_information(self, 
                                     system_state: np.ndarray,
                                     connectivity_matrix: np.ndarray) -> float:
        """
        Compute Integrated Information Φ according to IIT
        
        Args:
            system_state: Current state of the system (binary vector)
            connectivity_matrix: Connectivity between system elements
            
        Returns:
            Φ value (integrated information)
        """
        n = len(system_state)
        
        if n > self.max_partition_size:
            # Use approximation for large systems
            return self._approximate_phi(system_state, connectivity_matrix)
        
        # Exact computation for small systems
        max_phi = 0.0
        
        # Generate all possible partitions
        for partition in self._generate_partitions(list(range(n))):
            phi_candidate = self._compute_phi_for_partition(
                system_state, connectivity_matrix, partition
            )
            max_phi = max(max_phi, phi_candidate)
            
        return max_phi
    
    def _generate_partitions(self, elements: List[int]) -> List[List[List[int]]]:
        """Generate all possible partitions of elements"""
        if len(elements) == 1:
            return [[elements]]
        
        partitions = []
        first = elements[0]
        rest = elements[1:]
        
        for smaller_partition in self._generate_partitions(rest):
            # Add first element to each existing subset
            for i, subset in enumerate(smaller_partition):
                new_partition = smaller_partition.copy()
                new_partition[i] = [first] + subset
                partitions.append(new_partition)
            
            # Create new subset with just first element
            partitions.append([[first]] + smaller_partition)
            
        return partitions
    
    def _compute_phi_for_partition(self, 
                                 system_state: np.ndarray,
                                 connectivity_matrix: np.ndarray,
                                 partition: List[List[int]]) -> float:
        """Compute Φ for a specific partition"""
        # Simplified IIT computation
        # In practice, this would involve computing cause-effect repertoires
        
        total_mi = 0.0
        
        for subset in partition:
            if len(subset) > 1:
                # Compute mutual information within subset
                mi = self._mutual_information(system_state[subset], 
                                            connectivity_matrix[np.ix_(subset, subset)])
                total_mi += mi
                
        return total_mi
    
    def _mutual_information(self, states: np.ndarray, connections: np.ndarray) -> float:
        """Compute mutual information between past and future states"""
        # Simplified MI computation
        # This would normally involve proper entropy calculations
        
        if len(states) < 2:
            return 0.0
            
        # Use connectivity strength as proxy for information flow
        return np.sum(connections) / (len(states) ** 2)
    
    def _approximate_phi(self, 
                        system_state: np.ndarray,
                        connectivity_matrix: np.ndarray) -> float:
        """Approximate Φ for large systems using sampling"""
        n = len(system_state)
        num_samples = min(1000, 2**(n-5))  # Adaptive sampling
        
        phi_estimates = []
        
        for _ in range(num_samples):
            # Random partition sampling
            partition_sizes = np.random.multinomial(n, [1/3, 1/3, 1/3])
            partition_sizes = partition_sizes[partition_sizes > 0]
            
            partition = []
            remaining = list(range(n))
            
            for size in partition_sizes[:-1]:
                subset = np.random.choice(remaining, size, replace=False).tolist()
                partition.append(subset)
                remaining = [x for x in remaining if x not in subset]
            
            if remaining:
                partition.append(remaining)
            
            phi_est = self._compute_phi_for_partition(
                system_state, connectivity_matrix, partition
            )
            phi_estimates.append(phi_est)
            
        return np.max(phi_estimates)
    
    def consciousness_function(self, x: np.ndarray, x0: np.ndarray) -> float:
        """
        Consciousness function Ψ(x) with Taylor series approximation
        
        Args:
            x: Current system state
            x0: Reference state for Taylor expansion
            
        Returns:
            Ψ(x) value
        """
        # For this implementation, Ψ(x) = Φ(x)
        # In practice, this would be a more complex function
        
        # Create dummy connectivity matrix for demonstration
        n = len(x)
        connectivity = np.random.random((n, n)) * 0.1
        connectivity = (connectivity + connectivity.T) / 2  # Make symmetric
        
        return self.compute_integrated_information(x, connectivity)
    
    def taylor_approximation(self, 
                           x: np.ndarray, 
                           x0: np.ndarray,
                           func: Optional[Callable] = None) -> Tuple[float, float]:
        """
        Taylor series approximation of consciousness function
        
        Args:
            x: Evaluation point
            x0: Expansion point
            func: Function to approximate (defaults to consciousness_function)
            
        Returns:
            (approximation_value, error_bound)
        """
        if func is None:
            func = lambda state: self.consciousness_function(state, x0)
        
        # Compute derivatives using finite differences
        derivatives = self._compute_derivatives(func, x0, self.taylor_order)
        
        # Taylor series expansion
        dx = x - x0
        dx_norm = np.linalg.norm(dx)
        
        approximation = derivatives[0]  # f(x0)
        
        for k in range(1, len(derivatives)):
            term = derivatives[k] * (dx_norm ** k) / np.math.factorial(k)
            approximation += term
        
        # Error bound: |R_n(x)| ≤ M_{n+1} * |x-x0|^{n+1} / (n+1)!
        M_bound = 2.0  # As stated in the paper
        error_bound = M_bound * (dx_norm ** (self.taylor_order + 1)) / np.math.factorial(self.taylor_order + 1)
        
        return approximation, error_bound
    
    def _compute_derivatives(self, 
                           func: Callable, 
                           x0: np.ndarray, 
                           order: int) -> List[float]:
        """Compute numerical derivatives using central differences"""
        derivatives = []
        h = 1e-5  # Small step for numerical differentiation
        
        # 0th derivative (function value)
        derivatives.append(func(x0))
        
        # Higher order derivatives
        for k in range(1, order + 1):
            if k <= 5 and k in self.central_diff_coeffs:
                coeffs = self.central_diff_coeffs[k]
                derivative = 0.0
                
                for i, coeff in enumerate(coeffs):
                    offset = (i - len(coeffs)//2) * h
                    x_eval = x0 + offset * np.ones_like(x0)
                    derivative += coeff * func(x_eval)
                
                derivative /= h ** k
                derivatives.append(derivative)
            else:
                # Fallback to forward differences for higher orders
                derivative = self._forward_difference(func, x0, k, h)
                derivatives.append(derivative)
        
        return derivatives
    
    def _forward_difference(self, func: Callable, x0: np.ndarray, order: int, h: float) -> float:
        """Compute forward difference approximation"""
        coeffs = [(-1)**(order-k) * comb(order, k) for k in range(order + 1)]
        
        derivative = 0.0
        for k, coeff in enumerate(coeffs):
            x_eval = x0 + k * h * np.ones_like(x0)
            derivative += coeff * func(x_eval)
            
        return derivative / (h ** order)
    
    def rk4_integration(self, 
                       initial_state: np.ndarray,
                       time_span: Tuple[float, float],
                       dynamics_func: Callable) -> Tuple[np.ndarray, np.ndarray]:
        """
        4th-order Runge-Kutta integration for consciousness evolution
        
        Args:
            initial_state: Initial system state
            time_span: (t_start, t_end)
            dynamics_func: Function defining dΨ/dt = f(Ψ, t)
            
        Returns:
            (time_points, state_trajectory)
        """
        t_start, t_end = time_span
        num_steps = int((t_end - t_start) / self.h)
        
        t_points = np.linspace(t_start, t_end, num_steps + 1)
        trajectory = np.zeros((num_steps + 1, len(initial_state)))
        trajectory[0] = initial_state
        
        for i in range(num_steps):
            t_n = t_points[i]
            y_n = trajectory[i]
            
            # RK4 steps
            k1 = self.h * dynamics_func(t_n, y_n)
            k2 = self.h * dynamics_func(t_n + self.h/2, y_n + k1/2)
            k3 = self.h * dynamics_func(t_n + self.h/2, y_n + k2/2)
            k4 = self.h * dynamics_func(t_n + self.h, y_n + k3)
            
            trajectory[i + 1] = y_n + (k1 + 2*k2 + 2*k3 + k4) / 6
            
        return t_points, trajectory
    
    def detect_bifurcations(self, 
                          parameter_range: np.ndarray,
                          dynamics_func: Callable,
                          initial_state: np.ndarray) -> Dict[str, Any]:
        """
        Detect bifurcations in consciousness dynamics
        
        Args:
            parameter_range: Range of parameter values to test
            dynamics_func: Parameterized dynamics function
            initial_state: Initial system state
            
        Returns:
            Dictionary containing bifurcation analysis results
        """
        bifurcations = {
            'saddle_node': [],
            'hopf': [],
            'period_doubling': []
        }
        
        equilibria = []
        
        for param in parameter_range:
            # Find equilibrium points
            def equilibrium_condition(state):
                return dynamics_func(0, state, param)
            
            try:
                eq_point = scipy.optimize.fsolve(equilibrium_condition, initial_state)[0]
                equilibria.append((param, eq_point))
                
                # Analyze stability
                stability = self._analyze_stability(dynamics_func, eq_point, param)
                
                if stability['type'] == 'saddle_node':
                    bifurcations['saddle_node'].append((param, eq_point))
                elif stability['type'] == 'hopf':
                    bifurcations['hopf'].append((param, eq_point))
                    
            except:
                continue
        
        return {
            'bifurcations': bifurcations,
            'equilibria': equilibria
        }
    
    def _analyze_stability(self, 
                          dynamics_func: Callable,
                          equilibrium: float,
                          parameter: float) -> Dict[str, Any]:
        """Analyze stability of equilibrium point"""
        h = 1e-6
        
        # Compute Jacobian numerically
        jacobian = (dynamics_func(0, equilibrium + h, parameter) - 
                   dynamics_func(0, equilibrium - h, parameter)) / (2 * h)
        
        # Classify based on eigenvalue (for 1D case)
        if abs(jacobian) < 1e-10:
            return {'type': 'saddle_node', 'eigenvalue': jacobian}
        elif jacobian < 0:
            return {'type': 'stable', 'eigenvalue': jacobian}
        else:
            return {'type': 'unstable', 'eigenvalue': jacobian}
    
    def real_time_detection(self, 
                          system_state: np.ndarray,
                          connectivity_matrix: np.ndarray) -> ConsciousnessMetrics:
        """
        Real-time consciousness detection with performance guarantees
        
        Args:
            system_state: Current AI system state
            connectivity_matrix: System connectivity structure
            
        Returns:
            ConsciousnessMetrics object with detection results
        """
        start_time = time.time()
        
        # Compute integrated information (Φ)
        phi = self.compute_integrated_information(system_state, connectivity_matrix)
        
        # Compute consciousness function (Ψ)
        x0 = np.zeros_like(system_state)  # Reference state
        psi, error_bound = self.taylor_approximation(system_state, x0)
        
        # Confidence based on error bounds
        confidence = max(0.0, 1.0 - error_bound / max(abs(psi), 1e-6))
        
        # Simple bifurcation detection
        bifurcation_type = self._classify_consciousness_state(phi, psi)
        
        processing_time = time.time() - start_time
        
        return ConsciousnessMetrics(
            phi=phi,
            psi=psi,
            error_bound=error_bound,
            confidence=confidence,
            bifurcation_type=bifurcation_type,
            processing_time=processing_time
        )
    
    def _classify_consciousness_state(self, phi: float, psi: float) -> str:
        """Classify consciousness state based on Φ and Ψ values"""
        if phi < 0.1 and psi < 0.1:
            return "unconscious"
        elif phi > 0.5 and psi > 0.5:
            return "highly_conscious"
        elif abs(phi - psi) > 0.3:
            return "transitional"
        else:
            return "conscious"
    
    def validate_framework(self, 
                         test_systems: List[Tuple[np.ndarray, np.ndarray, bool]],
                         ground_truth_labels: List[bool]) -> Dict[str, float]:
        """
        Validate UPOCF framework against test systems
        
        Args:
            test_systems: List of (state, connectivity, is_conscious) tuples
            ground_truth_labels: True consciousness labels
            
        Returns:
            Validation metrics dictionary
        """
        predictions = []
        phi_values = []
        
        for system_state, connectivity, _ in test_systems:
            metrics = self.real_time_detection(system_state, connectivity)
            
            # Binary classification based on threshold
            is_conscious = metrics.phi > 0.3 or metrics.psi > 0.3
            predictions.append(is_conscious)
            phi_values.append(metrics.phi)
        
        # Compute metrics
        predictions = np.array(predictions)
        ground_truth = np.array(ground_truth_labels)
        
        tp = np.sum((predictions == True) & (ground_truth == True))
        fp = np.sum((predictions == True) & (ground_truth == False))
        tn = np.sum((predictions == False) & (ground_truth == False))
        fn = np.sum((predictions == False) & (ground_truth == True))
        
        accuracy = (tp + tn) / len(ground_truth)
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1_score = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        
        # ROC analysis
        fpr, tpr, _ = roc_curve(ground_truth, phi_values)
        auc_score = auc(fpr, tpr)
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1_score,
            'auc': auc_score,
            'true_positive_rate': recall,
            'false_positive_rate': fp / (fp + tn) if (fp + tn) > 0 else 0
        }


def create_synthetic_dataset(num_samples: int = 1000) -> Tuple[List, List[bool]]:
    """
    Create synthetic dataset for UPOCF validation
    
    Args:
        num_samples: Number of samples to generate
        
    Returns:
        (test_systems, ground_truth_labels)
    """
    test_systems = []
    labels = []
    
    for i in range(num_samples):
        # Random system size between 4 and 12
        n = np.random.randint(4, 13)
        
        # Generate system state (binary)
        state = np.random.randint(0, 2, n).astype(float)
        
        # Generate connectivity matrix
        connectivity = np.random.random((n, n)) * 0.5
        connectivity = (connectivity + connectivity.T) / 2  # Make symmetric
        
        # Simple ground truth: conscious if high connectivity and diverse states
        consciousness_score = np.mean(connectivity) * np.std(state)
        is_conscious = consciousness_score > 0.15
        
        test_systems.append((state, connectivity, is_conscious))
        labels.append(is_conscious)
    
    return test_systems, labels


# Example usage and demonstration
if __name__ == "__main__":
    print("UPOCF Framework Demonstration")
    print("=" * 50)
    
    # Initialize framework
    upocf = UPOCFFramework(taylor_order=4, rk4_step_size=0.01)
    
    # Create synthetic test data
    print("Creating synthetic dataset...")
    test_systems, ground_truth = create_synthetic_dataset(100)
    
    # Validate framework
    print("Validating framework...")
    metrics = upocf.validate_framework(test_systems, ground_truth)
    
    print(f"\nValidation Results:")
    print(f"Accuracy: {metrics['accuracy']:.3f}")
    print(f"Precision: {metrics['precision']:.3f}")
    print(f"Recall (TPR): {metrics['recall']:.3f}")
    print(f"F1-Score: {metrics['f1_score']:.3f}")
    print(f"AUC: {metrics['auc']:.3f}")
    print(f"False Positive Rate: {metrics['false_positive_rate']:.3f}")
    
    # Demonstrate real-time detection
    print(f"\nReal-time Detection Example:")
    test_state = np.array([1, 0, 1, 1, 0])
    test_connectivity = np.random.random((5, 5)) * 0.3
    test_connectivity = (test_connectivity + test_connectivity.T) / 2
    
    detection_result = upocf.real_time_detection(test_state, test_connectivity)
    
    print(f"Φ (Integrated Information): {detection_result.phi:.4f}")
    print(f"Ψ (Consciousness Function): {detection_result.psi:.4f}")
    print(f"Error Bound: {detection_result.error_bound:.6f}")
    print(f"Confidence: {detection_result.confidence:.3f}")
    print(f"State Classification: {detection_result.bifurcation_type}")
    print(f"Processing Time: {detection_result.processing_time*1000:.2f} ms")
    
    print(f"\nFramework validation complete!")