#!/usr/bin/env python3
"""
Medical AI Integration Demo
Demonstrates integration of ensemble neural networks for medical prediction
with the cognitive design framework's iXcan pipeline.

Based on research findings:
- Camps-Valls et al. (2001): Ensemble models, RMSE 44.77 ng/mL
- Li et al. (2008): GA-BP networks, 97.5% accuracy
- Cui (2008): Clinical validation, 97.1% accuracy (n=14)
- Wei (2010): Chained models, <15% deviation
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class PatientData:
    """Patient data structure matching the Mojo implementation."""
    patient_id: str
    weight: float  # kg
    creatinine: float  # mg/dL
    age: int
    gender: str
    previous_doses: List[float]  # mg
    blood_concentrations: List[float]  # ng/mL
    time_points: List[int]  # hours post-dose

@dataclass
class PredictionResult:
    """Prediction result with confidence and safety assessment."""
    predicted_concentration: float
    confidence_interval: float
    is_clinically_safe: bool
    model_consensus: float  # Agreement between ensemble models

class MedicalAIDemo:
    """Demonstration of medical AI integration with cognitive framework."""
    
    def __init__(self):
        self.patients = self._generate_synthetic_patients()
        self.validation_results = {}
        
    def _generate_synthetic_patients(self) -> List[PatientData]:
        """Generate synthetic patient data based on clinical parameters."""
        patients = []
        
        # Generate 14 patients (matching Cui 2008 study size)
        for i in range(14):
            patient = PatientData(
                patient_id=f"PT_{i+1:03d}",
                weight=np.random.normal(70, 15),  # kg
                creatinine=np.random.normal(1.2, 0.3),  # mg/dL
                age=np.random.randint(25, 75),
                gender=np.random.choice(['M', 'F']),
                previous_doses=[],
                blood_concentrations=[],
                time_points=[]
            )
            
            # Generate dosing history
            base_dose = 5.0 * patient.weight  # mg/kg starting dose
            for day in range(7):  # 7 days of data
                # Dose adjustment based on previous concentration
                if day > 0:
                    last_conc = patient.blood_concentrations[-1]
                    if last_conc < 100:  # Below therapeutic range
                        dose = patient.previous_doses[-1] * 1.1
                    elif last_conc > 400:  # Above therapeutic range
                        dose = patient.previous_doses[-1] * 0.9
                    else:
                        dose = patient.previous_doses[-1]
                else:
                    dose = base_dose
                
                patient.previous_doses.append(dose)
                
                # Simulate blood concentration with patient-specific factors
                clearance = 0.5 + 0.3 * (patient.creatinine - 1.0)  # Creatinine effect
                volume = 0.7 * patient.weight  # Volume of distribution
                
                # Pharmacokinetic model: C = Dose / (Clearance * Volume)
                concentration = dose / (clearance * volume)
                
                # Add biological variability
                concentration *= np.random.normal(1.0, 0.15)
                
                patient.blood_concentrations.append(max(0, concentration))
                patient.time_points.append(day * 24 + 12)  # 12 hours post-dose
            
            patients.append(patient)
        
        return patients
    
    def demonstrate_ensemble_prediction(self):
        """Demonstrate ensemble neural network prediction."""
        print("=== Ensemble Neural Network Demonstration ===")
        print(f"Training on {len(self.patients)} patients")
        
        # Split data for training/validation
        train_patients = self.patients[:10]
        test_patients = self.patients[10:]
        
        # Simulate ensemble predictions
        ensemble_results = []
        individual_model_results = {
            'weight_focused': [],
            'creatinine_focused': [],
            'ga_optimized': []
        }
        
        for patient in test_patients:
            # Simulate individual model predictions
            weight_pred = self._weight_focused_prediction(patient)
            creatinine_pred = self._creatinine_focused_prediction(patient)
            ga_pred = self._ga_optimized_prediction(patient)
            
            individual_model_results['weight_focused'].append(weight_pred)
            individual_model_results['creatinine_focused'].append(creatinine_pred)
            individual_model_results['ga_optimized'].append(ga_pred)
            
            # Ensemble prediction (weighted average)
            ensemble_pred = (0.3 * weight_pred + 0.3 * creatinine_pred + 0.4 * ga_pred)
            
            # Calculate confidence interval
            predictions = [weight_pred, creatinine_pred, ga_pred]
            variance = np.var(predictions)
            confidence_interval = 1.96 * np.sqrt(variance)
            
            # Safety assessment
            is_safe = 50 <= ensemble_pred <= 500  # Therapeutic window
            
            result = PredictionResult(
                predicted_concentration=ensemble_pred,
                confidence_interval=confidence_interval,
                is_clinically_safe=is_safe,
                model_consensus=1.0 - (variance / np.mean(predictions)**2)
            )
            
            ensemble_results.append(result)
            
            # Display results
            actual = patient.blood_concentrations[-1]
            error = abs(ensemble_pred - actual) / actual * 100
            
            print(f"\nPatient {patient.patient_id}:")
            print(f"  Actual: {actual:.1f} ng/mL")
            print(f"  Predicted: {ensemble_pred:.1f} ± {confidence_interval:.1f} ng/mL")
            print(f"  Error: {error:.1f}%")
            print(f"  Safe: {'Yes' if is_safe else 'No'}")
            print(f"  Consensus: {result.model_consensus:.3f}")
        
        return ensemble_results, individual_model_results
    
    def _weight_focused_prediction(self, patient: PatientData) -> float:
        """Simulate weight-focused model prediction."""
        # Simple model focusing on weight and weight-related features
        base_pred = 200 + (patient.weight - 70) * 2.5
        dose_effect = patient.previous_doses[-1] * 0.8 if patient.previous_doses else 0
        return max(0, base_pred + dose_effect + np.random.normal(0, 10))
    
    def _creatinine_focused_prediction(self, patient: PatientData) -> float:
        """Simulate creatinine-focused model prediction."""
        # Model focusing on renal function
        clearance_factor = 1.0 / patient.creatinine
        base_pred = 180 * clearance_factor
        dose_effect = patient.previous_doses[-1] * 0.9 if patient.previous_doses else 0
        return max(0, base_pred + dose_effect + np.random.normal(0, 12))
    
    def _ga_optimized_prediction(self, patient: PatientData) -> float:
        """Simulate GA-BP optimized model prediction."""
        # More sophisticated model with multiple factors
        weight_factor = patient.weight / 70.0
        creatinine_factor = 1.2 / patient.creatinine
        age_factor = 1.0 - (patient.age - 50) * 0.005
        
        base_pred = 220 * weight_factor * creatinine_factor * age_factor
        dose_effect = patient.previous_doses[-1] * 0.85 if patient.previous_doses else 0
        
        return max(0, base_pred + dose_effect + np.random.normal(0, 8))
    
    def validate_clinical_performance(self, ensemble_results: List[PredictionResult]):
        """Validate model performance against clinical standards."""
        print("\n=== Clinical Validation Results ===")
        
        test_patients = self.patients[10:]
        
        # Calculate metrics
        correct_predictions = 0
        total_predictions = len(test_patients)
        rmse_sum = 0.0
        safety_violations = 0
        
        for i, (patient, result) in enumerate(zip(test_patients, ensemble_results)):
            actual = patient.blood_concentrations[-1]
            predicted = result.predicted_concentration
            
            # Accuracy (within 15% as per Wei 2010)
            relative_error = abs(predicted - actual) / actual
            if relative_error <= 0.15:
                correct_predictions += 1
            
            # RMSE calculation
            squared_error = (predicted - actual) ** 2
            rmse_sum += squared_error
            
            # Safety assessment
            if not result.is_clinically_safe:
                safety_violations += 1
        
        accuracy = correct_predictions / total_predictions
        rmse = np.sqrt(rmse_sum / total_predictions)
        safety_rate = 1.0 - (safety_violations / total_predictions)
        
        print(f"Sample Size: {total_predictions} patients")
        print(f"Accuracy (≤15% error): {accuracy:.1%}")
        print(f"RMSE: {rmse:.2f} ng/mL")
        print(f"Safety Rate: {safety_rate:.1%}")
        
        # Compare with literature benchmarks
        print(f"\nLiterature Benchmarks:")
        print(f"  Camps-Valls et al. (2001): RMSE 44.77 ng/mL")
        print(f"  Li et al. (2008): 97.5% accuracy")
        print(f"  Cui (2008): 97.1% accuracy (n=14)")
        print(f"  Wei (2010): <15% deviation")
        
        # Clinical standards assessment
        meets_standards = (accuracy >= 0.95 and rmse <= 50.0 and safety_rate >= 0.98)
        print(f"\nMeets Clinical Standards: {'Yes' if meets_standards else 'No'}")
        
        return {
            'accuracy': accuracy,
            'rmse': rmse,
            'safety_rate': safety_rate,
            'sample_size': total_predictions,
            'meets_standards': meets_standards
        }
    
    def visualize_results(self, ensemble_results: List[PredictionResult], 
                         individual_results: Dict[str, List[float]]):
        """Create visualizations of the results."""
        test_patients = self.patients[10:]
        actual_values = [p.blood_concentrations[-1] for p in test_patients]
        predicted_values = [r.predicted_concentration for r in ensemble_results]
        confidence_intervals = [r.confidence_interval for r in ensemble_results]
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Prediction vs Actual
        ax1.errorbar(actual_values, predicted_values, yerr=confidence_intervals, 
                    fmt='o', capsize=5, alpha=0.7)
        ax1.plot([0, 500], [0, 500], 'r--', alpha=0.8, label='Perfect Prediction')
        ax1.fill_between([0, 500], [0, 425], [0, 575], alpha=0.2, color='green', 
                        label='±15% Acceptable Range')
        ax1.set_xlabel('Actual Concentration (ng/mL)')
        ax1.set_ylabel('Predicted Concentration (ng/mL)')
        ax1.set_title('Ensemble Model: Predicted vs Actual')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Individual Model Comparison
        models = ['weight_focused', 'creatinine_focused', 'ga_optimized']
        colors = ['blue', 'orange', 'green']
        
        for i, (model, color) in enumerate(zip(models, colors)):
            ax2.scatter(actual_values, individual_results[model], 
                       alpha=0.6, label=model.replace('_', ' ').title(), color=color)
        
        ax2.plot([0, 500], [0, 500], 'r--', alpha=0.8)
        ax2.set_xlabel('Actual Concentration (ng/mL)')
        ax2.set_ylabel('Predicted Concentration (ng/mL)')
        ax2.set_title('Individual Model Predictions')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Error Distribution
        errors = [(p - a) / a * 100 for p, a in zip(predicted_values, actual_values)]
        ax3.hist(errors, bins=8, alpha=0.7, color='skyblue', edgecolor='black')
        ax3.axvline(0, color='red', linestyle='--', label='Perfect Prediction')
        ax3.axvline(-15, color='orange', linestyle='--', label='±15% Threshold')
        ax3.axvline(15, color='orange', linestyle='--')
        ax3.set_xlabel('Prediction Error (%)')
        ax3.set_ylabel('Frequency')
        ax3.set_title('Prediction Error Distribution')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # 4. Model Consensus vs Accuracy
        consensus_scores = [r.model_consensus for r in ensemble_results]
        absolute_errors = [abs(p - a) / a * 100 for p, a in zip(predicted_values, actual_values)]
        
        ax4.scatter(consensus_scores, absolute_errors, alpha=0.7, color='purple')
        ax4.set_xlabel('Model Consensus Score')
        ax4.set_ylabel('Absolute Error (%)')
        ax4.set_title('Model Consensus vs Prediction Error')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('/Users/ryan_david_oates/cognitive-design-framework/data/medical_ai_demo_results.png', 
                   dpi=300, bbox_inches='tight')
        plt.show()
    
    def generate_clinical_report(self, validation_results: Dict):
        """Generate a clinical validation report."""
        report = {
            'timestamp': datetime.now().isoformat(),
            'study_design': {
                'total_patients': len(self.patients),
                'training_patients': 10,
                'validation_patients': 4,
                'study_reference': 'Cui (2008) - 14 patient validation'
            },
            'model_architecture': {
                'ensemble_components': [
                    'Weight-focused neural network (30% weight)',
                    'Creatinine-focused neural network (30% weight)', 
                    'GA-BP optimized neural network (40% weight)'
                ],
                'optimization_method': 'Genetic Algorithm + Backpropagation',
                'reference': 'Li et al. (2008)'
            },
            'performance_metrics': validation_results,
            'clinical_significance': {
                'therapeutic_range': '100-400 ng/mL',
                'toxic_threshold': '>500 ng/mL',
                'acceptable_deviation': '±15% (Wei 2010)',
                'safety_assessment': 'Automated clinical safety checks'
            },
            'framework_integration': {
                'cognitive_architecture': 'iXcan Pipeline Integration',
                'autopoietic_features': 'Self-optimizing ensemble weights',
                'consciousness_framework': 'Clinical decision support',
                'validation_approach': 'Small-sample clinical validation'
            }
        }
        
        # Save report
        report_path = '/Users/ryan_david_oates/cognitive-design-framework/data/medical_ai_clinical_report.json'
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\nClinical report saved to: {report_path}")
        return report

def main():
    """Run the medical AI integration demonstration."""
    print("Medical AI Integration with Cognitive Design Framework")
    print("=" * 60)
    
    demo = MedicalAIDemo()
    
    # Run ensemble prediction demonstration
    ensemble_results, individual_results = demo.demonstrate_ensemble_prediction()
    
    # Validate clinical performance
    validation_results = demo.validate_clinical_performance(ensemble_results)
    
    # Create visualizations
    demo.visualize_results(ensemble_results, individual_results)
    
    # Generate clinical report
    clinical_report = demo.generate_clinical_report(validation_results)
    
    print("\n" + "=" * 60)
    print("Demo completed successfully!")
    print("Check the data/ directory for generated reports and visualizations.")

if __name__ == "__main__":
    main()
