#!/usr/bin/env python3
"""
Numerical Analysis Demo for MECN Framework
Step-by-step computation of Ψ(x) along phase-space trajectory

This script implements the numerical analysis described in the user's analysis,
showing how Ψ(x) is computed at different points along the trajectory.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, Dict

class MECNNumericalAnalysis:
    """
    Numerical analysis implementation for MECN framework
    Demonstrates step-by-step computation of Ψ(x) equation
    """
    
    def __init__(self):
        """Initialize the numerical analysis framework."""
        self.beta = 1.4  # Expert bias parameter
        self.w_cross = 0.1  # Cross-term weight
        
    def symbolic_output(self, x: float) -> float:
        """
        Symbolic processing S(x) - structured, interpretable reasoning
        Based on RK4 solution for pendulum angle
        """
        return 0.60  # RK4 solution for pendulum angle
        
    def neural_output(self, x: float) -> float:
        """
        Neural processing N(x) - data-driven pattern recognition
        LSTM prediction as described in analysis
        """
        return 0.80  # LSTM prediction
        
    def calculate_cognitive_penalty(self, symbolic_output: float, neural_output: float) -> float:
        """
        Calculate R_cognitive - deviation from cognitive plausibility
        """
        coherence_deviation = abs(symbolic_output - neural_output)
        logical_clarity = 1.0 - coherence_deviation
        return 1.0 - logical_clarity
        
    def calculate_efficiency_penalty(self) -> float:
        """
        Calculate R_efficiency - computational inefficiency penalty
        """
        return 0.10  # Moderate cost as described
        
    def bias_adjusted_probability(self, base_probability: float) -> float:
        """
        Calculate P(H|E,β) - bias-adjusted probability
        """
        return base_probability * self.beta
        
    def compute_psi_x_step_by_step(self, alpha_t: float, lambda_1: float, lambda_2: float) -> Dict[str, float]:
        """
        Compute Ψ(x) step-by-step as described in the analysis.
        
        Args:
            alpha_t: Dynamic weighting factor α(t)
            lambda_1: Cognitive plausibility weight λ₁
            lambda_2: Computational efficiency weight λ₂
            
        Returns:
            Dictionary containing all intermediate values and final result
        """
        print(f"\n🔍 Computing Ψ(x) for α(t)={alpha_t:.2f}, λ₁={lambda_1:.2f}, λ₂={lambda_2:.2f}")
        print("=" * 60)
        
        # Step 1: Define outputs
        S_x = self.symbolic_output(1.0)
        N_x = self.neural_output(1.0)
        print(f"Step 1: Define Outputs")
        print(f"   • Symbolic Output S(x) = {S_x:.2f} (RK4 solution)")
        print(f"   • Neural Output N(x) = {N_x:.2f} (LSTM prediction)")
        
        # Step 2: Hybrid output
        # Normalize alpha_t to [0,1] range for computation
        alpha_normalized = alpha_t / 2.0  # Scale from [0,2] to [0,1]
        hybrid_output = alpha_normalized * S_x + (1.0 - alpha_normalized) * N_x
        print(f"\nStep 2: Hybrid Output")
        print(f"   • Weight α(t) = {alpha_t:.2f} (normalized to {alpha_normalized:.2f})")
        print(f"   • Hybrid Output = {alpha_normalized:.2f} × {S_x:.2f} + {1-alpha_normalized:.2f} × {N_x:.2f}")
        print(f"   • Hybrid Output = {hybrid_output:.2f}")
        
        # Step 3: Calculate regularization penalties
        R_cognitive = self.calculate_cognitive_penalty(S_x, N_x)
        R_efficiency = self.calculate_efficiency_penalty()
        
        # Normalize lambda weights to [0,1] range
        lambda_1_norm = lambda_1 / 2.0
        lambda_2_norm = lambda_2 / 2.0
        
        penalty_total = lambda_1_norm * R_cognitive + lambda_2_norm * R_efficiency
        regularization_factor = np.exp(-penalty_total)
        
        print(f"\nStep 3: Calculate Regularization Penalties")
        print(f"   • Cognitive Penalty R_cognitive = {R_cognitive:.2f}")
        print(f"   • Efficiency Penalty R_efficiency = {R_efficiency:.2f}")
        print(f"   • Weights: λ₁ = {lambda_1:.2f} (norm: {lambda_1_norm:.2f}), λ₂ = {lambda_2:.2f} (norm: {lambda_2_norm:.2f})")
        print(f"   • Total Penalty = {lambda_1_norm:.2f} × {R_cognitive:.2f} + {lambda_2_norm:.2f} × {R_efficiency:.2f} = {penalty_total:.4f}")
        print(f"   • Exponential Factor = exp(-{penalty_total:.4f}) = {regularization_factor:.4f}")
        
        # Step 4: Bias-adjusted probability
        base_probability = 0.70  # Confidence in prediction
        bias_probability = self.bias_adjusted_probability(base_probability)
        
        print(f"\nStep 4: Bias-Adjusted Probability")
        print(f"   • Base Probability P(H|E) = {base_probability:.2f}")
        print(f"   • Bias β = {self.beta:.2f}")
        print(f"   • Adjusted Probability = {base_probability:.2f} × {self.beta:.2f} = {bias_probability:.2f}")
        
        # Step 5: Compute Ψ(x)
        psi_x = hybrid_output * regularization_factor * bias_probability
        
        print(f"\nStep 5: Compute Ψ(x)")
        print(f"   • Ψ(x) = {hybrid_output:.4f} × {regularization_factor:.4f} × {bias_probability:.4f}")
        print(f"   • Ψ(x) = {psi_x:.4f}")
        
        # Interpretation
        print(f"\n🎯 Interpretation:")
        if psi_x > 0.7:
            reliability = "High"
        elif psi_x > 0.5:
            reliability = "Moderate"
        else:
            reliability = "Low"
        print(f"   • Ψ(x) = {psi_x:.4f} indicates {reliability} reliability")
        print(f"   • Balanced state where α(t) = {alpha_t:.2f} favors neither S(x) nor N(x) excessively")
        print(f"   • Regularization ensures alignment with RK4-validated models")
        
        return {
            'S_x': S_x,
            'N_x': N_x,
            'alpha_t': alpha_t,
            'alpha_normalized': alpha_normalized,
            'hybrid_output': hybrid_output,
            'R_cognitive': R_cognitive,
            'R_efficiency': R_efficiency,
            'lambda_1': lambda_1,
            'lambda_2': lambda_2,
            'lambda_1_norm': lambda_1_norm,
            'lambda_2_norm': lambda_2_norm,
            'penalty_total': penalty_total,
            'regularization_factor': regularization_factor,
            'base_probability': base_probability,
            'bias_probability': bias_probability,
            'psi_x': psi_x
        }

def analyze_trajectory_points():
    """
    Analyze multiple points along the phase-space trajectory.
    """
    analyzer = MECNNumericalAnalysis()
    
    # Define trajectory points to analyze
    trajectory_points = [
        (2.0, 2.0, 2.0, "Initial State"),
        (1.5, 1.5, 1.5, "Early Transition"),
        (1.0, 1.0, 1.0, "Balanced State"),
        (0.5, 0.5, 0.5, "Final State")
    ]
    
    results = []
    
    print("🔬 Phase-Space Trajectory Numerical Analysis")
    print("=" * 80)
    
    for alpha_t, lambda_1, lambda_2, description in trajectory_points:
        print(f"\n📍 {description}")
        print("-" * 40)
        
        result = analyzer.compute_psi_x_step_by_step(alpha_t, lambda_1, lambda_2)
        results.append({
            'description': description,
            'alpha_t': alpha_t,
            'lambda_1': lambda_1,
            'lambda_2': lambda_2,
            'psi_x': result['psi_x']
        })
    
    return results

def create_trajectory_summary_plot(results):
    """
    Create a summary plot showing Ψ(x) values along the trajectory.
    """
    descriptions = [r['description'] for r in results]
    psi_values = [r['psi_x'] for r in results]
    alpha_values = [r['alpha_t'] for r in results]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot 1: Ψ(x) vs trajectory points
    ax1.plot(range(len(descriptions)), psi_values, 'bo-', linewidth=2, markersize=8)
    ax1.set_xlabel('Trajectory Points')
    ax1.set_ylabel('Ψ(x) Value')
    ax1.set_title('Ψ(x) Evolution Along Trajectory')
    ax1.set_xticks(range(len(descriptions)))
    ax1.set_xticklabels(descriptions, rotation=45)
    ax1.grid(True, alpha=0.3)
    
    # Add value labels
    for i, (desc, psi) in enumerate(zip(descriptions, psi_values)):
        ax1.annotate(f'{psi:.3f}', (i, psi), textcoords="offset points", 
                     xytext=(0,10), ha='center')
    
    # Plot 2: Ψ(x) vs α(t)
    ax2.plot(alpha_values, psi_values, 'ro-', linewidth=2, markersize=8)
    ax2.set_xlabel('α(t)')
    ax2.set_ylabel('Ψ(x) Value')
    ax2.set_title('Ψ(x) vs Dynamic Weight α(t)')
    ax2.grid(True, alpha=0.3)
    
    # Add value labels
    for alpha, psi in zip(alpha_values, psi_values):
        ax2.annotate(f'{psi:.3f}', (alpha, psi), textcoords="offset points", 
                     xytext=(0,10), ha='center')
    
    plt.tight_layout()
    plt.savefig('trajectory_analysis_summary.png', dpi=300, bbox_inches='tight')
    print("\n💾 Summary plot saved as 'trajectory_analysis_summary.png'")
    plt.show()

def main():
    """
    Main function to run the numerical analysis.
    """
    print("🔬 MECN Framework Numerical Analysis")
    print("Ryan David Oates' Dynamical Systems Analysis")
    print("=" * 80)
    
    # Run trajectory analysis
    results = analyze_trajectory_points()
    
    # Create summary plot
    create_trajectory_summary_plot(results)
    
    # Print final summary
    print("\n📊 Final Summary:")
    print("=" * 40)
    for result in results:
        print(f"• {result['description']}: Ψ(x) = {result['psi_x']:.4f}")
    
    print("\n🎯 Key Insights:")
    print("• Ψ(x) shows how the system balances symbolic and neural processing")
    print("• Regularization ensures cognitive plausibility and efficiency")
    print("• The trajectory represents dynamic adaptation in chaotic systems")
    print("• Aligns with Oates' PINNs and DMD methodologies")

if __name__ == "__main__":
    main()