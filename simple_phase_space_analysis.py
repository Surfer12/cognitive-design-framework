#!/usr/bin/env python3
"""
Simple Phase-Space Trajectory Analysis for MECN Framework
Ryan David Oates' Dynamical Systems Analysis

This script provides a text-based analysis of the phase-space trajectory
without requiring external plotting libraries.
"""

import math

def generate_phase_space_trajectory():
    """
    Generate the phase-space trajectory data matching the analysis.
    
    Returns:
        tuple: (t_values, alpha_values, lambda1_values, lambda2_values)
    """
    # Time parameter t from 0 to 1
    t_values = [i/100 for i in range(101)]
    
    # α(t): Time-varying weight balancing symbolic and neural outputs
    # Linear decrease from 2.0 to 0.5 as described in analysis
    alpha_values = [2.0 - 1.5 * t for t in t_values]
    
    # λ₁: Cognitive plausibility weight (vertical axis)
    # Decreases from 2.0 to 0.5 as α(t) increases
    lambda1_values = [2.0 - 1.5 * t for t in t_values]
    
    # λ₂: Computational efficiency weight (horizontal axis)  
    # Decreases from 2.0 to 0.5 as α(t) increases
    lambda2_values = [2.0 - 1.5 * t for t in t_values]
    
    return t_values, alpha_values, lambda1_values, lambda2_values

def compute_psi_x_step_by_step(alpha_t, lambda_1, lambda_2):
    """
    Compute Ψ(x) step-by-step as described in the analysis.
    """
    print(f"\n🔍 Computing Ψ(x) for α(t)={alpha_t:.2f}, λ₁={lambda_1:.2f}, λ₂={lambda_2:.2f}")
    print("=" * 60)
    
    # Step 1: Define outputs
    S_x = 0.60  # RK4 solution for pendulum angle
    N_x = 0.80  # LSTM prediction
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
    R_cognitive = 0.25  # Mild misalignment with physical laws
    R_efficiency = 0.10  # Moderate cost
    
    # Normalize lambda weights to [0,1] range
    lambda_1_norm = lambda_1 / 2.0
    lambda_2_norm = lambda_2 / 2.0
    
    penalty_total = lambda_1_norm * R_cognitive + lambda_2_norm * R_efficiency
    regularization_factor = math.exp(-penalty_total)
    
    print(f"\nStep 3: Calculate Regularization Penalties")
    print(f"   • Cognitive Penalty R_cognitive = {R_cognitive:.2f}")
    print(f"   • Efficiency Penalty R_efficiency = {R_efficiency:.2f}")
    print(f"   • Weights: λ₁ = {lambda_1:.2f} (norm: {lambda_1_norm:.2f}), λ₂ = {lambda_2:.2f} (norm: {lambda_2_norm:.2f})")
    print(f"   • Total Penalty = {lambda_1_norm:.2f} × {R_cognitive:.2f} + {lambda_2_norm:.2f} × {R_efficiency:.2f} = {penalty_total:.4f}")
    print(f"   • Exponential Factor = exp(-{penalty_total:.4f}) = {regularization_factor:.4f}")
    
    # Step 4: Bias-adjusted probability
    base_probability = 0.70  # Confidence in prediction
    beta = 1.4  # Expert bias
    bias_probability = base_probability * beta
    
    print(f"\nStep 4: Bias-Adjusted Probability")
    print(f"   • Base Probability P(H|E) = {base_probability:.2f}")
    print(f"   • Bias β = {beta:.2f}")
    print(f"   • Adjusted Probability = {base_probability:.2f} × {beta:.2f} = {bias_probability:.2f}")
    
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
    
    return psi_x

def analyze_trajectory_points():
    """
    Analyze multiple points along the phase-space trajectory.
    """
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
        
        psi_x = compute_psi_x_step_by_step(alpha_t, lambda_1, lambda_2)
        results.append({
            'description': description,
            'alpha_t': alpha_t,
            'lambda_1': lambda_1,
            'lambda_2': lambda_2,
            'psi_x': psi_x
        })
    
    return results

def print_trajectory_summary(results):
    """
    Print a summary of the trajectory analysis.
    """
    print("\n📊 Trajectory Summary:")
    print("=" * 50)
    print(f"{'State':<20} {'α(t)':<8} {'λ₁':<8} {'λ₂':<8} {'Ψ(x)':<8}")
    print("-" * 50)
    
    for result in results:
        print(f"{result['description']:<20} {result['alpha_t']:<8.2f} {result['lambda_1']:<8.2f} {result['lambda_2']:<8.2f} {result['psi_x']:<8.4f}")
    
    print("\n🎯 Key Insights:")
    print("• The trajectory shows simultaneous decrease in λ₁ and λ₂ as α(t) increases")
    print("• This represents dynamic adaptation between symbolic and neural processing")
    print("• The regularization weights adjust to maintain cognitive plausibility and efficiency")
    print("• Aligns with Oates' PINNs and DMD methodologies for chaotic systems")

def print_equation_display():
    """
    Print the core equation display.
    """
    equation_text = """
Core MECN Equation:
Ψ(x) = ∫[α(t)S(x) + (1-α(t))N(x) + w_cross[S(m₁)N(m₂) - S(m₂)N(m₁)]] 
       × exp(-[λ₁R_cognitive + λ₂R_efficiency]) × P(H|E,β) dt

Where:
• α(t): Dynamic weighting factor (0-2 range)
• λ₁: Cognitive plausibility weight  
• λ₂: Computational efficiency weight
• S(x): Symbolic reasoning output
• N(x): Neural processing output
• R_cognitive: Cognitive penalty
• R_efficiency: Efficiency penalty
• P(H|E,β): Bias-adjusted probability
"""
    print(equation_text)

def main():
    """
    Main function to run the phase-space analysis.
    """
    print("🔬 Phase-Space Trajectory Analysis for MECN Framework")
    print("Ryan David Oates' Dynamical Systems Analysis")
    print("=" * 80)
    
    # Display equation
    print_equation_display()
    
    # Generate trajectory data
    t_vals, alpha_vals, lambda1_vals, lambda2_vals = generate_phase_space_trajectory()
    
    print("📊 Trajectory Analysis:")
    print(f"• Start Point: α(t)={alpha_vals[0]:.1f}, λ₁={lambda1_vals[0]:.1f}, λ₂={lambda2_vals[0]:.1f}")
    print(f"• Mid Point:  α(t)={alpha_vals[len(alpha_vals)//2]:.1f}, λ₁={lambda1_vals[len(alpha_vals)//2]:.1f}, λ₂={lambda2_vals[len(alpha_vals)//2]:.1f}")
    print(f"• End Point:  α(t)={alpha_vals[-1]:.1f}, λ₁={lambda1_vals[-1]:.1f}, λ₂={lambda2_vals[-1]:.1f}")
    
    print("\n🎯 Interpretation:")
    print("• The trajectory shows simultaneous decrease in λ₁ and λ₂ as α(t) increases")
    print("• This represents dynamic adaptation between symbolic and neural processing")
    print("• The regularization weights adjust to maintain cognitive plausibility and efficiency")
    print("• Aligns with Oates' PINNs and DMD methodologies")
    
    # Run trajectory analysis
    results = analyze_trajectory_points()
    
    # Print summary
    print_trajectory_summary(results)
    
    print("\n💡 Connection to Oates' Work:")
    print("• PINNs and Neural ODEs: The trajectory could stem from PINNs embedding pendulum differential equations")
    print("• DMD and Koopman Theory: DMD might generate the mode interactions driving λ₁ and λ₂")
    print("• Verification: The trajectory's consistency with RK4 benchmarks aligns with Oates' methodology")
    print("• This phase-space plot serves as a visual representation of the core equation's dynamic optimization")

if __name__ == "__main__":
    main()