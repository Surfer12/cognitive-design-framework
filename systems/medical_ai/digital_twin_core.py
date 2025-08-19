#!/usr/bin/env python3
"""
Digital Twin Core System
Real-time, AI-driven digital twin for personalized drug dosing

Implements the novel approach described by OpenAI:
- Hybrid neural architectures (GNN + RNN + Transformers)
- Reinforcement learning for policy optimization
- Bayesian uncertainty quantification
- Real-time adaptation and learning

Integrates with the cognitive design framework's autopoietic systems.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json
from abc import ABC, abstractmethod

@dataclass
class PatientState:
    """Complete patient state representation for digital twin."""
    patient_id: str
    timestamp: datetime
    
    # Demographics
    age: float
    weight: float
    height: float
    sex: str
    
    # Genomics (key pharmacogenomic markers)
    cyp3a4_genotype: str  # *1/*1, *1/*22, etc.
    cyp3a5_genotype: str
    abcb1_genotype: str
    
    # Clinical parameters
    creatinine: float
    bun: float
    liver_enzymes: Dict[str, float]
    blood_pressure: Tuple[float, float]
    heart_rate: float
    
    # Drug history
    current_medications: List[Dict[str, Any]]
    dose_history: List[Tuple[datetime, float]]  # (timestamp, dose)
    concentration_history: List[Tuple[datetime, float]]  # (timestamp, concentration)
    
    # Sensor data (from wearables/IoT)
    adherence_score: float  # 0-1
    activity_level: float
    sleep_quality: float
    
    # Clinical outcomes
    rejection_episodes: List[datetime]
    adverse_events: List[Dict[str, Any]]
    
    # Uncertainty tracking
    data_completeness: float  # 0-1
    measurement_reliability: Dict[str, float]

@dataclass
class TreatmentAction:
    """Represents a treatment decision/action."""
    action_type: str  # "dose_change", "drug_switch", "monitoring_increase"
    parameters: Dict[str, Any]
    confidence: float
    expected_outcome: Dict[str, float]
    risk_assessment: Dict[str, float]
    
@dataclass
class DigitalTwinPrediction:
    """Enhanced prediction with uncertainty and causal reasoning."""
    predicted_concentration: float
    concentration_ci: Tuple[float, float]  # 95% confidence interval
    
    recommended_dose: float
    dose_ci: Tuple[float, float]
    
    # Uncertainty quantification
    epistemic_uncertainty: float  # Model uncertainty
    aleatoric_uncertainty: float  # Data uncertainty
    total_uncertainty: float
    
    # Causal reasoning
    counterfactual_outcomes: Dict[str, float]  # What-if scenarios
    causal_confidence: float
    
    # Safety assessment
    toxicity_risk: float
    efficacy_probability: float
    therapeutic_window_probability: float
    
    # Explanation
    key_factors: List[Tuple[str, float]]  # (factor_name, importance)
    recommendation_rationale: str

class CognitiveDigitalTwin:
    """
    Core digital twin system implementing real-time personalized medicine.
    
    Integrates with the cognitive design framework's autopoietic principles:
    - Self-maintenance through continuous learning
    - Self-organization through adaptive architecture
    - Boundary management through patient-specific models
    """
    
    def __init__(self, patient_id: str):
        self.patient_id = patient_id
        self.creation_time = datetime.now()
        self.last_update = datetime.now()
        
        # Patient state tracking
        self.current_state: Optional[PatientState] = None
        self.state_history: List[PatientState] = []
        
        # Learning components
        self.neural_engine = HybridNeuralEngine()
        self.rl_agent = ReinforcementLearningAgent()
        self.bayesian_layer = BayesianUncertaintyLayer()
        self.causal_engine = CausalInferenceEngine()
        
        # Autopoietic properties
        self.adaptation_rate = 0.1
        self.stability_threshold = 0.95
        self.learning_momentum = 0.9
        
        # Performance tracking
        self.prediction_history: List[DigitalTwinPrediction] = []
        self.accuracy_metrics: Dict[str, List[float]] = {
            'concentration_mae': [],
            'dose_accuracy': [],
            'safety_score': []
        }
        
    def update_patient_state(self, new_data: Dict[str, Any]) -> None:
        """Update patient state with new real-time data."""
        
        # Create new patient state
        if self.current_state is None:
            # Initialize first state
            self.current_state = self._initialize_patient_state(new_data)
        else:
            # Update existing state
            self.current_state = self._update_state(self.current_state, new_data)
        
        # Store in history
        self.state_history.append(self.current_state)
        
        # Trigger autopoietic adaptation
        self._adapt_to_new_data()
        
        self.last_update = datetime.now()
        
    def _initialize_patient_state(self, data: Dict[str, Any]) -> PatientState:
        """Initialize patient state from first data point."""
        
        return PatientState(
            patient_id=self.patient_id,
            timestamp=datetime.now(),
            age=data.get('age', 50.0),
            weight=data.get('weight', 70.0),
            height=data.get('height', 170.0),
            sex=data.get('sex', 'M'),
            cyp3a4_genotype=data.get('cyp3a4', '*1/*1'),
            cyp3a5_genotype=data.get('cyp3a5', '*1/*3'),
            abcb1_genotype=data.get('abcb1', 'CC'),
            creatinine=data.get('creatinine', 1.0),
            bun=data.get('bun', 20.0),
            liver_enzymes=data.get('liver_enzymes', {'ALT': 30, 'AST': 25}),
            blood_pressure=data.get('bp', (120, 80)),
            heart_rate=data.get('hr', 70),
            current_medications=data.get('medications', []),
            dose_history=data.get('dose_history', []),
            concentration_history=data.get('concentration_history', []),
            adherence_score=data.get('adherence', 1.0),
            activity_level=data.get('activity', 0.5),
            sleep_quality=data.get('sleep', 0.8),
            rejection_episodes=data.get('rejections', []),
            adverse_events=data.get('adverse_events', []),
            data_completeness=self._calculate_completeness(data),
            measurement_reliability=data.get('reliability', {})
        )
    
    def _update_state(self, current: PatientState, new_data: Dict[str, Any]) -> PatientState:
        """Update existing patient state with new data."""
        
        # Create updated state (simplified - in practice would be more sophisticated)
        updated_state = PatientState(
            patient_id=current.patient_id,
            timestamp=datetime.now(),
            age=current.age,  # Demographics don't change rapidly
            weight=new_data.get('weight', current.weight),
            height=current.height,
            sex=current.sex,
            cyp3a4_genotype=current.cyp3a4_genotype,
            cyp3a5_genotype=current.cyp3a5_genotype,
            abcb1_genotype=current.abcb1_genotype,
            creatinine=new_data.get('creatinine', current.creatinine),
            bun=new_data.get('bun', current.bun),
            liver_enzymes=new_data.get('liver_enzymes', current.liver_enzymes),
            blood_pressure=new_data.get('bp', current.blood_pressure),
            heart_rate=new_data.get('hr', current.heart_rate),
            current_medications=new_data.get('medications', current.current_medications),
            dose_history=current.dose_history + new_data.get('new_doses', []),
            concentration_history=current.concentration_history + new_data.get('new_concentrations', []),
            adherence_score=new_data.get('adherence', current.adherence_score),
            activity_level=new_data.get('activity', current.activity_level),
            sleep_quality=new_data.get('sleep', current.sleep_quality),
            rejection_episodes=current.rejection_episodes + new_data.get('new_rejections', []),
            adverse_events=current.adverse_events + new_data.get('new_adverse_events', []),
            data_completeness=self._calculate_completeness(new_data),
            measurement_reliability=new_data.get('reliability', current.measurement_reliability)
        )
        
        return updated_state
    
    def _calculate_completeness(self, data: Dict[str, Any]) -> float:
        """Calculate data completeness score."""
        required_fields = ['creatinine', 'weight', 'adherence']
        available = sum(1 for field in required_fields if field in data)
        return available / len(required_fields)
    
    def _adapt_to_new_data(self) -> None:
        """Autopoietic adaptation to new data."""
        
        if len(self.state_history) < 2:
            return
        
        # Detect significant changes
        current = self.current_state
        previous = self.state_history[-2]
        
        # Calculate change magnitude
        changes = {
            'creatinine': abs(current.creatinine - previous.creatinine) / previous.creatinine,
            'weight': abs(current.weight - previous.weight) / previous.weight,
            'adherence': abs(current.adherence_score - previous.adherence_score)
        }
        
        # Adapt learning rate based on change magnitude
        max_change = max(changes.values())
        if max_change > 0.1:  # Significant change
            self.adaptation_rate = min(0.3, self.adaptation_rate * 1.2)
        else:
            self.adaptation_rate = max(0.05, self.adaptation_rate * 0.95)
        
        # Update neural engine with new adaptation rate
        self.neural_engine.set_learning_rate(self.adaptation_rate)
    
    def predict_and_recommend(self, target_concentration: float = 250.0) -> DigitalTwinPrediction:
        """Generate prediction and treatment recommendation."""
        
        if self.current_state is None:
            raise ValueError("No patient state available for prediction")
        
        # Neural engine prediction
        neural_pred = self.neural_engine.predict(self.current_state)
        
        # Bayesian uncertainty quantification
        uncertainty = self.bayesian_layer.quantify_uncertainty(
            self.current_state, neural_pred
        )
        
        # Reinforcement learning recommendation
        rl_action = self.rl_agent.recommend_action(
            self.current_state, target_concentration
        )
        
        # Causal inference for counterfactuals
        counterfactuals = self.causal_engine.generate_counterfactuals(
            self.current_state, rl_action
        )
        
        # Safety assessment
        safety = self._assess_safety(neural_pred, rl_action)
        
        # Create comprehensive prediction
        prediction = DigitalTwinPrediction(
            predicted_concentration=neural_pred['concentration'],
            concentration_ci=uncertainty['concentration_ci'],
            recommended_dose=rl_action['dose'],
            dose_ci=uncertainty['dose_ci'],
            epistemic_uncertainty=uncertainty['epistemic'],
            aleatoric_uncertainty=uncertainty['aleatoric'],
            total_uncertainty=uncertainty['total'],
            counterfactual_outcomes=counterfactuals,
            causal_confidence=uncertainty['causal_confidence'],
            toxicity_risk=safety['toxicity_risk'],
            efficacy_probability=safety['efficacy_prob'],
            therapeutic_window_probability=safety['therapeutic_prob'],
            key_factors=neural_pred['feature_importance'],
            recommendation_rationale=self._generate_rationale(neural_pred, rl_action, safety)
        )
        
        # Store prediction for learning
        self.prediction_history.append(prediction)
        
        return prediction
    
    def _assess_safety(self, neural_pred: Dict, rl_action: Dict) -> Dict[str, float]:
        """Assess safety of predicted outcomes."""
        
        predicted_conc = neural_pred['concentration']
        
        # Toxicity risk (concentration > 400 ng/mL)
        toxicity_risk = max(0, (predicted_conc - 400) / 100) if predicted_conc > 400 else 0
        
        # Efficacy probability (concentration > 100 ng/mL)
        efficacy_prob = min(1, predicted_conc / 100) if predicted_conc < 100 else 1
        
        # Therapeutic window (100-400 ng/mL)
        if 100 <= predicted_conc <= 400:
            therapeutic_prob = 1.0
        elif predicted_conc < 100:
            therapeutic_prob = predicted_conc / 100
        else:
            therapeutic_prob = max(0, (500 - predicted_conc) / 100)
        
        return {
            'toxicity_risk': min(1.0, toxicity_risk),
            'efficacy_prob': efficacy_prob,
            'therapeutic_prob': therapeutic_prob
        }
    
    def _generate_rationale(self, neural_pred: Dict, rl_action: Dict, safety: Dict) -> str:
        """Generate human-readable rationale for recommendation."""
        
        rationale_parts = []
        
        # Primary factors
        top_factors = sorted(neural_pred['feature_importance'], key=lambda x: abs(x[1]), reverse=True)[:3]
        factor_text = ", ".join([f"{factor} ({importance:.2f})" for factor, importance in top_factors])
        rationale_parts.append(f"Key factors: {factor_text}")
        
        # Safety assessment
        if safety['toxicity_risk'] > 0.3:
            rationale_parts.append("⚠️ Elevated toxicity risk - consider dose reduction")
        elif safety['efficacy_prob'] < 0.7:
            rationale_parts.append("⚠️ Subtherapeutic risk - consider dose increase")
        else:
            rationale_parts.append("✅ Within therapeutic window")
        
        # Confidence
        total_uncertainty = neural_pred.get('uncertainty', 0.1)
        if total_uncertainty < 0.1:
            rationale_parts.append("High confidence prediction")
        elif total_uncertainty > 0.3:
            rationale_parts.append("⚠️ High uncertainty - recommend additional monitoring")
        
        return ". ".join(rationale_parts)
    
    def learn_from_outcome(self, actual_concentration: float, actual_outcome: Dict[str, Any]) -> None:
        """Learn from actual patient outcomes (autopoietic learning)."""
        
        if not self.prediction_history:
            return
        
        # Get most recent prediction
        last_prediction = self.prediction_history[-1]
        
        # Calculate prediction error
        conc_error = abs(last_prediction.predicted_concentration - actual_concentration)
        relative_error = conc_error / actual_concentration
        
        # Update accuracy metrics
        self.accuracy_metrics['concentration_mae'].append(conc_error)
        
        # Reward/penalty for RL agent
        reward = self._calculate_reward(actual_concentration, actual_outcome)
        self.rl_agent.update_policy(reward)
        
        # Update neural engine with new data point
        self.neural_engine.online_update(self.current_state, actual_concentration)
        
        # Bayesian update
        self.bayesian_layer.update_beliefs(last_prediction, actual_concentration)
        
        # Autopoietic adaptation based on performance
        if relative_error > 0.2:  # Poor prediction
            self.adaptation_rate = min(0.5, self.adaptation_rate * 1.5)
        else:  # Good prediction
            self.adaptation_rate = max(0.05, self.adaptation_rate * 0.9)
    
    def _calculate_reward(self, actual_concentration: float, outcome: Dict[str, Any]) -> float:
        """Calculate reward for reinforcement learning."""
        
        reward = 0.0
        
        # Therapeutic window reward
        if 100 <= actual_concentration <= 400:
            reward += 1.0
        elif actual_concentration < 100:
            reward -= (100 - actual_concentration) / 100
        else:  # > 400
            reward -= (actual_concentration - 400) / 100
        
        # Outcome-based rewards
        if outcome.get('rejection', False):
            reward -= 2.0
        if outcome.get('toxicity', False):
            reward -= 1.5
        if outcome.get('stable', True):
            reward += 0.5
        
        return reward
    
    def get_twin_status(self) -> Dict[str, Any]:
        """Get current status of the digital twin."""
        
        return {
            'patient_id': self.patient_id,
            'creation_time': self.creation_time.isoformat(),
            'last_update': self.last_update.isoformat(),
            'state_history_length': len(self.state_history),
            'prediction_count': len(self.prediction_history),
            'current_adaptation_rate': self.adaptation_rate,
            'average_accuracy': np.mean(self.accuracy_metrics['concentration_mae']) if self.accuracy_metrics['concentration_mae'] else None,
            'data_completeness': self.current_state.data_completeness if self.current_state else None,
            'autopoietic_health': self._assess_autopoietic_health()
        }
    
    def _assess_autopoietic_health(self) -> Dict[str, float]:
        """Assess the health of the autopoietic system."""
        
        health = {
            'learning_stability': 0.8,  # Placeholder
            'adaptation_efficiency': min(1.0, 1.0 / (1.0 + self.adaptation_rate)),
            'prediction_consistency': 0.9,  # Placeholder
            'data_integration': self.current_state.data_completeness if self.current_state else 0.0
        }
        
        health['overall'] = np.mean(list(health.values()))
        return health

# Placeholder classes for the component systems
class HybridNeuralEngine:
    """Hybrid neural network combining GNN, RNN, and Transformers."""
    
    def __init__(self):
        self.learning_rate = 0.001
        
    def set_learning_rate(self, lr: float):
        self.learning_rate = lr
        
    def predict(self, state: PatientState) -> Dict[str, Any]:
        # Simplified prediction - in practice would use actual neural networks
        base_conc = 200 + (state.weight - 70) * 2 + (1.2 - state.creatinine) * 50
        
        # Add some realistic variation
        concentration = max(0, base_conc + np.random.normal(0, 20))
        
        return {
            'concentration': concentration,
            'feature_importance': [
                ('weight', 0.3),
                ('creatinine', 0.4),
                ('adherence', 0.2),
                ('age', 0.1)
            ],
            'uncertainty': 0.15
        }
    
    def online_update(self, state: PatientState, actual_concentration: float):
        # Placeholder for online learning
        pass

class ReinforcementLearningAgent:
    """RL agent for dose optimization."""
    
    def __init__(self):
        self.policy_weights = np.random.normal(0, 0.1, 10)
        
    def recommend_action(self, state: PatientState, target_conc: float) -> Dict[str, Any]:
        # Simplified dose recommendation
        current_dose = state.dose_history[-1][1] if state.dose_history else 300
        
        # Simple policy: adjust based on last concentration
        if state.concentration_history:
            last_conc = state.concentration_history[-1][1]
            if last_conc < target_conc * 0.8:
                recommended_dose = current_dose * 1.1
            elif last_conc > target_conc * 1.2:
                recommended_dose = current_dose * 0.9
            else:
                recommended_dose = current_dose
        else:
            recommended_dose = 5.0 * state.weight  # Standard starting dose
        
        return {
            'dose': recommended_dose,
            'confidence': 0.8
        }
    
    def update_policy(self, reward: float):
        # Placeholder for policy update
        pass

class BayesianUncertaintyLayer:
    """Bayesian layer for uncertainty quantification."""
    
    def quantify_uncertainty(self, state: PatientState, prediction: Dict) -> Dict[str, Any]:
        # Simplified uncertainty quantification
        base_uncertainty = 0.1
        
        # Increase uncertainty with incomplete data
        data_penalty = (1.0 - state.data_completeness) * 0.2
        
        # Increase uncertainty with limited history
        history_penalty = max(0, (5 - len(state.concentration_history)) * 0.05)
        
        total_uncertainty = base_uncertainty + data_penalty + history_penalty
        
        predicted_conc = prediction['concentration']
        ci_width = total_uncertainty * predicted_conc
        
        return {
            'epistemic': base_uncertainty,
            'aleatoric': data_penalty + history_penalty,
            'total': total_uncertainty,
            'concentration_ci': (predicted_conc - ci_width, predicted_conc + ci_width),
            'dose_ci': (250, 350),  # Placeholder
            'causal_confidence': 0.7
        }
    
    def update_beliefs(self, prediction: DigitalTwinPrediction, actual: float):
        # Placeholder for Bayesian update
        pass

class CausalInferenceEngine:
    """Causal inference for counterfactual reasoning."""
    
    def generate_counterfactuals(self, state: PatientState, action: Dict) -> Dict[str, float]:
        # Simplified counterfactual generation
        base_conc = action.get('dose', 300) * 0.8  # Simple dose-concentration relationship
        
        return {
            'no_treatment': 50,
            'double_dose': base_conc * 1.8,
            'half_dose': base_conc * 0.6,
            'perfect_adherence': base_conc * 1.1,
            'poor_adherence': base_conc * 0.7
        }
