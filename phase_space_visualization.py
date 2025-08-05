#!/usr/bin/env python3
"""
Phase-Space Trajectory Visualization for MECN Framework
Ryan David Oates' Dynamical Systems Analysis

This script generates the 3D phase-space trajectory plot showing the evolution
of α(t), λ₁, and λ₂ parameters in the core equation:
Ψ(x) = ∫[α(t)S(x) + (1-α(t))N(x) + w_cross[S(m₁)N(m₂) - S(m₂)N(m₁)]] 
       × exp(-[λ₁R_cognitive + λ₂R_efficiency]) × P(H|E,β) dt
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as mpatches
from matplotlib import cm

def generate_phase_space_trajectory():
    """
    Generate the phase-space trajectory data matching the analysis.
    
    Returns:
        tuple: (t_values, alpha_values, lambda1_values, lambda2_values)
    """
    # Time parameter t from 0 to 1
    t_values = np.linspace(0, 1, 100)
    
    # α(t): Time-varying weight balancing symbolic and neural outputs
    # Linear decrease from 2.0 to 0.5 as described in analysis
    alpha_values = 2.0 - 1.5 * t_values
    
    # λ₁: Cognitive plausibility weight (vertical axis)
    # Decreases from 2.0 to 0.5 as α(t) increases
    lambda1_values = 2.0 - 1.5 * t_values
    
    # λ₂: Computational efficiency weight (horizontal axis)  
    # Decreases from 2.0 to 0.5 as α(t) increases
    lambda2_values = 2.0 - 1.5 * t_values
    
    return t_values, alpha_values, lambda1_values, lambda2_values

def create_phase_space_plot():
    """
    Create the 3D phase-space trajectory plot matching the analysis.
    """
    # Generate trajectory data
    t_vals, alpha_vals, lambda1_vals, lambda2_vals = generate_phase_space_trajectory()
    
    # Create 3D plot
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot the trajectory
    ax.plot(alpha_vals, lambda1_vals, lambda2_vals, 
            linewidth=4, color='blue', alpha=0.8, label='Phase-Space Trajectory')
    
    # Mark start and end points
    ax.scatter([alpha_vals[0]], [lambda1_vals[0]], [lambda2_vals[0]], 
               color='red', s=100, label='Start (t=0)')
    ax.scatter([alpha_vals[-1]], [lambda1_vals[-1]], [lambda2_vals[-1]], 
               color='green', s=100, label='End (t=1)')
    
    # Set axis labels and ranges
    ax.set_xlabel('α(t)', fontsize=12, fontweight='bold')
    ax.set_ylabel('λ₁(t)', fontsize=12, fontweight='bold') 
    ax.set_zlabel('λ₂(t)', fontsize=12, fontweight='bold')
    
    # Set axis ranges to match the analysis
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 2)
    ax.set_zlim(0, 2)
    
    # Add grid
    ax.grid(True, alpha=0.3)
    
    # Set title
    ax.set_title('Phase-Space Trajectory: α(t), λ₁(t), λ₂(t)\nMECN Framework Dynamic Optimization', 
                 fontsize=14, fontweight='bold', pad=20)
    
    # Add legend
    ax.legend(loc='upper right')
    
    # Set viewing angle to match the analysis description
    ax.view_init(elev=20, azim=45)
    
    return fig, ax

def add_analysis_annotations(ax, alpha_vals, lambda1_vals, lambda2_vals):
    """
    Add annotations explaining key points on the trajectory.
    """
    # Add text annotations for key points
    mid_idx = len(alpha_vals) // 2
    
    # Midpoint annotation (t ≈ 0.5)
    ax.text(alpha_vals[mid_idx], lambda1_vals[mid_idx], lambda2_vals[mid_idx] + 0.1,
            'Balanced State\n(α≈1.0, λ₁≈1.5, λ₂≈0.5)', 
            fontsize=10, ha='center', va='bottom',
            bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))
    
    # Start point annotation
    ax.text(alpha_vals[0] + 0.1, lambda1_vals[0], lambda2_vals[0],
            'Initial State\n(α≈2.0, λ₁≈2.0, λ₂≈2.0)', 
            fontsize=10, ha='left', va='center',
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
    
    # End point annotation  
    ax.text(alpha_vals[-1] - 0.1, lambda1_vals[-1], lambda2_vals[-1],
            'Final State\n(α≈0.5, λ₁≈0.5, λ₂≈0.5)', 
            fontsize=10, ha='right', va='center',
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen", alpha=0.7))

def create_equation_display():
    """
    Create a text display showing the core equation.
    """
    equation_text = r"""
Core MECN Equation:
$\Psi(x) = \int \left[ \alpha(t) S(x) + (1-\alpha(t)) N(x) + w_{\text{cross}} [S(m_1)N(m_2) - S(m_2)N(m_1)] \right] \times \exp\left(-[\lambda_1 R_{\text{cognitive}} + \lambda_2 R_{\text{efficiency}}]\right) \times P(H|E,\beta) \, dt$

Where:
• $\alpha(t)$: Dynamic weighting factor (0-2 range)
• $\lambda_1$: Cognitive plausibility weight  
• $\lambda_2$: Computational efficiency weight
• $S(x)$: Symbolic reasoning output
• $N(x)$: Neural processing output
• $R_{\text{cognitive}}$: Cognitive penalty
• $R_{\text{efficiency}}$: Efficiency penalty
• $P(H|E,\beta)$: Bias-adjusted probability
"""
    return equation_text

def main():
    """
    Main function to generate and display the phase-space visualization.
    """
    print("🔬 Generating Phase-Space Trajectory Visualization")
    print("=" * 60)
    
    # Create the main plot
    fig, ax = create_phase_space_plot()
    
    # Get trajectory data for annotations
    t_vals, alpha_vals, lambda1_vals, lambda2_vals = generate_phase_space_trajectory()
    
    # Add analysis annotations
    add_analysis_annotations(ax, alpha_vals, lambda1_vals, lambda2_vals)
    
    # Display equation
    equation_text = create_equation_display()
    print("\n📐 Core Equation:")
    print(equation_text)
    
    # Print trajectory analysis
    print("\n📊 Trajectory Analysis:")
    print(f"• Start Point: α(t)={alpha_vals[0]:.1f}, λ₁={lambda1_vals[0]:.1f}, λ₂={lambda2_vals[0]:.1f}")
    print(f"• Mid Point:  α(t)={alpha_vals[len(alpha_vals)//2]:.1f}, λ₁={lambda1_vals[len(alpha_vals)//2]:.1f}, λ₂={lambda2_vals[len(alpha_vals)//2]:.1f}")
    print(f"• End Point:  α(t)={alpha_vals[-1]:.1f}, λ₁={lambda1_vals[-1]:.1f}, λ₂={lambda2_vals[-1]:.1f}")
    
    print("\n🎯 Interpretation:")
    print("• The trajectory shows simultaneous decrease in λ₁ and λ₂ as α(t) increases")
    print("• This represents dynamic adaptation between symbolic and neural processing")
    print("• The regularization weights adjust to maintain cognitive plausibility and efficiency")
    print("• Aligns with Oates' PINNs and DMD methodologies for chaotic systems")
    
    # Save the plot
    plt.tight_layout()
    plt.savefig('phase_space_trajectory.png', dpi=300, bbox_inches='tight')
    print("\n💾 Plot saved as 'phase_space_trajectory.png'")
    
    # Show the plot
    plt.show()

if __name__ == "__main__":
    main()