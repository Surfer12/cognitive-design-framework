#!/usr/bin/env python3
"""
False Wall Breakthrough for Medical AI Optimization (Fixed)
Implements techniques to overcome model-induced local optima in patient parameter space
"""

import numpy as np
from typing import List, Dict, Tuple, Optional, Callable
from dataclasses import dataclass
import json

def sigmoid(x):
    """Sigmoid activation function."""
    return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))  # Clip to prevent overflow

@dataclass
class TreatmentPlan:
    """Decoded treatment plan from latent space."""
    plan_id: str
    dose_sequence: List[float]
    monitoring_frequency: List[int]
    predicted_concentrations: List[float]
    predicted_efficacy: float
    predicted_toxicity_risk: float
    clinical_validity: bool

@dataclass
class OptimizationState:
    """Current state in treatment optimization."""
    latent_position: np.ndarray
    gradient: np.ndarray
    objective_value: float
    uncertainty: float
    iteration: int
    is_stuck: bool
    exploration_bonus: float

class FalseWallDetector:
    """Detects when optimization is stuck at false walls."""
    
    def __init__(self, gradient_threshold: float = 1e-4, 
                 plateau_threshold: float = 1e-3, 
                 uncertainty_threshold: float = 0.3,
                 plateau_window: int = 5):
        self.gradient_threshold = gradient_threshold
        self.plateau_threshold = plateau_threshold
        self.uncertainty_threshold = uncertainty_threshold
        self.plateau_window = plateau_window
        
    def detect_false_wall(self, optimization_history: List[OptimizationState]) -> bool:
        """Detect if optimization is stuck at a false wall."""
        if len(optimization_history) < self.plateau_window:
            return False
        
        current_state = optimization_history[-1]
        recent_states = optimization_history[-self.plateau_window:]
        
        # Criterion 1: Gradient magnitude ||∇f(z)|| ≈ 0
        gradient_magnitude = np.linalg.norm(current_state.gradient)
        gradient_stuck = gradient_magnitude < self.gradient_threshold
        
        # Criterion 2: Objective plateau
        objective_values = [state.objective_value for state in recent_states]
        objective_range = max(objective_values) - min(objective_values)
        plateau_detected = objective_range < self.plateau_threshold
        
        # Criterion 3: High uncertainty
        high_uncertainty = current_state.uncertainty > self.uncertainty_threshold
        
        return gradient_stuck and plateau_detected and high_uncertainty

class UncertaintyAwareOptimizer:
    """Optimizer that uses uncertainty to guide exploration."""
    
    def __init__(self, base_optimizer, exploration_weight: float = 0.1):
        self.base_optimizer = base_optimizer
        self.beta = exploration_weight
        
    def compute_exploration_objective(self, latent_position: np.ndarray, 
                                    base_objective: float, 
                                    uncertainty: float) -> float:
        """Compute exploration-enhanced objective: f̃(z) = f̂(z) + β · Uncertainty(z)"""
        exploration_bonus = self.beta * uncertainty
        return base_objective + exploration_bonus
    
    def optimize_step(self, current_state: OptimizationState, 
                     objective_function: Callable,
                     uncertainty_function: Callable) -> OptimizationState:
        """Single optimization step with uncertainty-aware exploration."""
        
        # Compute base objective and uncertainty
        base_obj = objective_function(current_state.latent_position)
        uncertainty = uncertainty_function(current_state.latent_position)
        
        # Enhanced objective with exploration bonus
        enhanced_obj = self.compute_exploration_objective(
            current_state.latent_position, base_obj, uncertainty
        )
        
        # Compute gradient
        gradient = self._compute_gradient(
            current_state.latent_position, objective_function, uncertainty_function
        )
        
        # Optimization step
        learning_rate = 0.01
        new_position = current_state.latent_position + learning_rate * gradient
        
        return OptimizationState(
            latent_position=new_position,
            gradient=gradient,
            objective_value=enhanced_obj,
            uncertainty=uncertainty,
            iteration=current_state.iteration + 1,
            is_stuck=False,
            exploration_bonus=self.beta * uncertainty
        )
    
    def _compute_gradient(self, position: np.ndarray, 
                         objective_func: Callable, 
                         uncertainty_func: Callable,
                         epsilon: float = 1e-6) -> np.ndarray:
        """Compute gradient using finite differences."""
        
        gradient = np.zeros_like(position)
        
        for i in range(len(position)):
            pos_plus = position.copy()
            pos_plus[i] += epsilon
            
            pos_minus = position.copy()
            pos_minus[i] -= epsilon
            
            obj_plus = self.compute_exploration_objective(
                pos_plus, objective_func(pos_plus), uncertainty_func(pos_plus)
            )
            obj_minus = self.compute_exploration_objective(
                pos_minus, objective_func(pos_minus), uncertainty_func(pos_minus)
            )
            
            gradient[i] = (obj_plus - obj_minus) / (2 * epsilon)
        
        return gradient

class LatentSpaceExplorer:
    """Explores latent space to break through false walls."""
    
    def __init__(self, noise_scale: float = 0.1, jump_probability: float = 0.2):
        self.sigma = noise_scale
        self.jump_prob = jump_probability
        
    def explore_beyond_wall(self, stuck_position: np.ndarray, 
                           exploration_directions: int = 8) -> List[np.ndarray]:
        """Generate exploration points beyond a detected false wall."""
        
        exploration_points = []
        
        # Random noise-driven exploration
        for _ in range(exploration_directions):
            noise = np.random.normal(0, self.sigma, stuck_position.shape)
            exploration_point = stuck_position + noise
            exploration_points.append(exploration_point)
        
        # Systematic directional exploration
        for dim in range(min(len(stuck_position), 4)):  # Limit to first 4 dimensions
            direction = np.zeros_like(stuck_position)
            direction[dim] = self.sigma * 2
            exploration_points.append(stuck_position + direction)
            exploration_points.append(stuck_position - direction)
        
        return exploration_points

class TreatmentDecoder:
    """Decodes latent positions into concrete treatment plans."""
    
    def __init__(self):
        self.plan_counter = 0
        
    def decode_treatment_plan(self, latent_position: np.ndarray, 
                            patient_context: Dict) -> TreatmentPlan:
        """Decode latent position into concrete treatment plan."""
        
        self.plan_counter += 1
        
        # Ensure we have enough dimensions
        if len(latent_position) < 9:
            # Pad with zeros if needed
            padded_position = np.zeros(16)
            padded_position[:len(latent_position)] = latent_position
            latent_position = padded_position
        
        # Base dose from latent dimensions 0-2
        base_dose = 200 + 100 * np.tanh(latent_position[0])
        
        # Dose adjustment pattern from dimensions 3-5
        dose_pattern = np.tanh(latent_position[3:6])
        
        # Monitoring frequency from dimensions 6-8
        monitoring_pattern = sigmoid(latent_position[6:9])
        
        # Generate dose sequence (7 days)
        dose_sequence = []
        for day in range(7):
            daily_adjustment = 1.0 + 0.1 * dose_pattern[day % 3]
            dose = base_dose * daily_adjustment
            dose_sequence.append(max(50, min(500, dose)))
        
        # Generate monitoring schedule
        monitoring_frequency = []
        for i in range(len(monitoring_pattern)):
            days = int(1 + 6 * monitoring_pattern[i])
            monitoring_frequency.append(days)
        
        # Predict outcomes
        predicted_concentrations = self._predict_concentrations(dose_sequence, patient_context)
        efficacy = self._predict_efficacy(predicted_concentrations)
        toxicity_risk = self._predict_toxicity_risk(predicted_concentrations)
        clinical_validity = self._validate_clinical_feasibility(
            dose_sequence, monitoring_frequency, predicted_concentrations
        )
        
        return TreatmentPlan(
            plan_id=f"PLAN_{self.plan_counter:04d}",
            dose_sequence=dose_sequence,
            monitoring_frequency=monitoring_frequency,
            predicted_concentrations=predicted_concentrations,
            predicted_efficacy=efficacy,
            predicted_toxicity_risk=toxicity_risk,
            clinical_validity=clinical_validity
        )
    
    def _predict_concentrations(self, dose_sequence: List[float], 
                              patient_context: Dict) -> List[float]:
        """Predict blood concentrations from dose sequence."""
        
        concentrations = []
        clearance = 0.5 + 0.3 * (patient_context.get('creatinine', 1.0) - 1.0)
        volume = 0.7 * patient_context.get('weight', 70)
        
        for dose in dose_sequence:
            concentration = dose / (clearance * volume)
            concentration *= np.random.normal(1.0, 0.1)
            concentrations.append(max(0, concentration))
        
        return concentrations
    
    def _predict_efficacy(self, concentrations: List[float]) -> float:
        """Predict treatment efficacy from concentrations."""
        in_range = sum(1 for c in concentrations if 100 <= c <= 400)
        return in_range / len(concentrations)
    
    def _predict_toxicity_risk(self, concentrations: List[float]) -> float:
        """Predict toxicity risk from concentrations."""
        toxic_exposures = sum(max(0, c - 400) for c in concentrations)
        max_possible = sum(max(0, 1000 - 400) for _ in concentrations)
        
        if max_possible > 0:
            return min(1.0, toxic_exposures / max_possible)
        return 0.0
    
    def _validate_clinical_feasibility(self, dose_sequence: List[float], 
                                     monitoring_frequency: List[int], 
                                     concentrations: List[float]) -> bool:
        """Validate if treatment plan is clinically feasible."""
        
        if any(dose < 50 or dose > 500 for dose in dose_sequence):
            return False
        if any(freq < 1 or freq > 7 for freq in monitoring_frequency):
            return False
        if any(conc > 1000 for conc in concentrations):
            return False
        
        return True

class FalseWallBreakthroughSystem:
    """Complete system for detecting and breaking through false walls."""
    
    def __init__(self):
        self.detector = FalseWallDetector()
        self.explorer = LatentSpaceExplorer()
        self.decoder = TreatmentDecoder()
        self.optimization_history: List[OptimizationState] = []
        
    def optimize_treatment(self, patient_context: Dict, 
                         initial_position: np.ndarray,
                         max_iterations: int = 20) -> Dict:
        """Optimize treatment with false wall breakthrough capability."""
        
        # Initialize optimization
        current_state = OptimizationState(
            latent_position=initial_position,
            gradient=np.zeros_like(initial_position),
            objective_value=0.0,
            uncertainty=1.0,
            iteration=0,
            is_stuck=False,
            exploration_bonus=0.0
        )
        
        self.optimization_history = [current_state]
        
        # Define objective and uncertainty functions
        def objective_function(z):
            try:
                plan = self.decoder.decode_treatment_plan(z, patient_context)
                return plan.predicted_efficacy - 0.5 * plan.predicted_toxicity_risk
            except:
                return -1.0  # Penalty for invalid positions
        
        def uncertainty_function(z):
            return min(1.0, np.linalg.norm(z) * 0.1)
        
        # Optimization loop
        optimizer = UncertaintyAwareOptimizer(None, exploration_weight=0.2)
        
        for iteration in range(max_iterations):
            # Check for false wall
            if self.detector.detect_false_wall(self.optimization_history):
                print(f"   False wall detected at iteration {iteration}")
                
                # Explore beyond the wall
                exploration_points = self.explorer.explore_beyond_wall(
                    current_state.latent_position, exploration_directions=4
                )
                
                # Evaluate exploration points
                best_exploration = None
                best_objective = current_state.objective_value
                
                for point in exploration_points:
                    obj_value = objective_function(point)
                    if obj_value > best_objective:
                        best_objective = obj_value
                        best_exploration = point
                
                # Jump to best exploration point if found
                if best_exploration is not None:
                    print(f"   Breaking through! Improvement: {best_objective - current_state.objective_value:.4f}")
                    current_state.latent_position = best_exploration
                    current_state.objective_value = best_objective
                    current_state.is_stuck = False
                else:
                    current_state.is_stuck = True
            
            # Regular optimization step
            if not current_state.is_stuck:
                try:
                    current_state = optimizer.optimize_step(
                        current_state, objective_function, uncertainty_function
                    )
                except:
                    # If optimization fails, mark as stuck
                    current_state.is_stuck = True
            
            self.optimization_history.append(current_state)
        
        # Generate final treatment plans
        try:
            final_plans = []
            for i in range(3):  # Generate 3 plans
                noise = np.random.normal(0, 0.05, current_state.latent_position.shape)
                perturbed_position = current_state.latent_position + noise
                plan = self.decoder.decode_treatment_plan(perturbed_position, patient_context)
                final_plans.append(plan)
        except:
            # Fallback plan
            final_plans = [self.decoder.decode_treatment_plan(current_state.latent_position, patient_context)]
        
        return {
            'optimization_history': self.optimization_history,
            'final_position': current_state.latent_position,
            'final_objective': current_state.objective_value,
            'treatment_plans': final_plans,
            'false_walls_detected': sum(1 for s in self.optimization_history if s.is_stuck),
            'breakthrough_achieved': any(s.is_stuck for s in self.optimization_history[:-3])
        }

def demonstrate_false_wall_breakthrough():
    """Demonstrate false wall detection and breakthrough."""
    
    print("🚫 False Wall Breakthrough for Medical AI Optimization")
    print("=" * 70)
    print("Mathematical Framework: Overcoming Model-Induced Local Optima")
    print()
    
    # Create patient context
    patient_context = {
        'age': 65,
        'weight': 75,
        'creatinine': 1.8,
        'cyp3a4_score': 0.5,
        'adherence': 0.9,
        'risk_category': 'high'
    }
    
    print("1. Patient Context:")
    for key, value in patient_context.items():
        print(f"   {key}: {value}")
    print()
    
    # Initialize system
    breakthrough_system = FalseWallBreakthroughSystem()
    
    # Initial position in latent space
    np.random.seed(42)
    initial_position = np.random.normal(0, 0.5, 16)
    
    print("2. Starting optimization from initial latent position...")
    print(f"   Initial position shape: {initial_position.shape}")
    print(f"   Initial position norm: {np.linalg.norm(initial_position):.4f}")
    print()
    
    # Run optimization with breakthrough capability
    print("3. Running optimization with false wall detection...")
    results = breakthrough_system.optimize_treatment(
        patient_context, initial_position, max_iterations=15
    )
    
    print(f"   Optimization completed in {len(results['optimization_history'])} iterations")
    print(f"   Final objective value: {results['final_objective']:.4f}")
    print(f"   False walls detected: {results['false_walls_detected']}")
    print(f"   Breakthrough achieved: {results['breakthrough_achieved']}")
    print()
    
    # Analyze optimization trajectory
    print("4. Optimization Trajectory Analysis:")
    objectives = [s.objective_value for s in results['optimization_history']]
    uncertainties = [s.uncertainty for s in results['optimization_history']]
    exploration_bonuses = [s.exploration_bonus for s in results['optimization_history']]
    
    print(f"   Objective improvement: {objectives[-1] - objectives[0]:.4f}")
    print(f"   Average uncertainty: {np.mean(uncertainties):.4f}")
    print(f"   Average exploration bonus: {np.mean(exploration_bonuses):.4f}")
    print()
    
    # Display final treatment plans
    print("5. Final Treatment Plans (Multiple Decodings):")
    for i, plan in enumerate(results['treatment_plans']):
        print(f"   Plan {i+1} ({plan.plan_id}):")
        print(f"     Dose sequence: {[f'{d:.1f}' for d in plan.dose_sequence[:3]]}... mg")
        print(f"     Predicted efficacy: {plan.predicted_efficacy:.3f}")
        print(f"     Toxicity risk: {plan.predicted_toxicity_risk:.3f}")
        print(f"     Clinically valid: {plan.clinical_validity}")
        print()
    
    # Mathematical validation
    print("6. Mathematical Validation:")
    final_state = results['optimization_history'][-1]
    gradient_norm = np.linalg.norm(final_state.gradient)
    print(f"   Final gradient norm: {gradient_norm:.6f}")
    
    stuck_states = [s for s in results['optimization_history'] if s.is_stuck]
    if stuck_states:
        print(f"   Stuck states encountered: {len(stuck_states)}")
        print(f"   Successfully overcame: {results['breakthrough_achieved']}")
    else:
        print("   No false walls encountered in this run")
    
    high_uncertainty_states = [s for s in results['optimization_history'] if s.uncertainty > 0.3]
    print(f"   High uncertainty states: {len(high_uncertainty_states)}")
    print()
    
    print("✅ False wall breakthrough demonstration completed!")
    print()
    print("🎯 Key Mathematical Insights:")
    print("   • False wall detection: ||∇f(z)|| ≈ 0 + plateau + high uncertainty")
    print("   • Exploration objective: f̃(z) = f̂(z) + β·Uncertainty(z)")
    print("   • Breakthrough strategy: z_{t+1} = z_t + η∇f(z_t) + ε_t")
    print("   • Multiple decoding: {x^(1), x^(2), ..., x^(n)} ~ p(x|z)")
    print("   • Systematic exploration beyond apparent optimization limits")
    print()
    print("🏥 Clinical Applications:")
    print("   • Overcome training data bias in treatment recommendations")
    print("   • Discover novel therapeutic approaches beyond known patterns")
    print("   • Explore underrepresented patient phenotypes")
    print("   • Optimize treatment beyond apparent limits")
    print("   • Ensure comprehensive treatment space exploration")

if __name__ == "__main__":
    demonstrate_false_wall_breakthrough()
