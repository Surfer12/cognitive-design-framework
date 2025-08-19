#!/usr/bin/env python3
"""
Neural Network Architectures for Two-Stage Pharmaceutical Modeling
Implements MLP, FIR, Elman RNN, and Ensemble approaches for drug prediction

Based on cyclosporine studies:
- Camps-Valls et al. (2001, 2003): Ensemble approaches, RMSE ~44 ng/mL
- Two-stage modeling: Concentration → Dosage prediction
"""

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import matplotlib.pyplot as plt

@dataclass
class PatientTimeSeries:
    """Time series data for a patient."""
    patient_id: str
    demographics: np.ndarray  # [age, weight, sex, creatinine, etc.]
    dose_history: np.ndarray  # Historical doses
    concentration_history: np.ndarray  # Historical blood concentrations
    time_points: np.ndarray  # Time stamps
    target_concentration: float  # Next concentration to predict
    target_dose: float  # Next dose to predict

class MLPNetwork(nn.Module):
    """Multilayer Perceptron for static tabular data prediction."""
    
    def __init__(self, input_size: int, hidden_sizes: List[int], output_size: int):
        super(MLPNetwork, self).__init__()
        
        layers = []
        prev_size = input_size
        
        for hidden_size in hidden_sizes:
            layers.extend([
                nn.Linear(prev_size, hidden_size),
                nn.ReLU(),
                nn.Dropout(0.2)
            ])
            prev_size = hidden_size
        
        layers.append(nn.Linear(prev_size, output_size))
        self.network = nn.Sequential(*layers)
        
    def forward(self, x):
        return self.network(x)

class FIRNeuralNetwork(nn.Module):
    """Finite Impulse Response Neural Network for short-term memory."""
    
    def __init__(self, input_size: int, fir_length: int, hidden_size: int, output_size: int):
        super(FIRNeuralNetwork, self).__init__()
        
        self.fir_length = fir_length
        self.input_size = input_size
        
        # FIR filter weights
        self.fir_weights = nn.Parameter(torch.randn(fir_length, input_size))
        
        # Neural network processing
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_size)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.2)
        
    def forward(self, x):
        # x shape: (batch_size, sequence_length, input_size)
        batch_size, seq_len, _ = x.shape
        
        # Apply FIR filtering
        if seq_len >= self.fir_length:
            # Take the last fir_length time steps
            recent_x = x[:, -self.fir_length:, :]
            
            # Apply FIR weights
            fir_output = torch.sum(recent_x * self.fir_weights.unsqueeze(0), dim=1)
        else:
            # If sequence is shorter, pad with zeros
            padded_x = torch.zeros(batch_size, self.fir_length, self.input_size)
            padded_x[:, -seq_len:, :] = x
            fir_output = torch.sum(padded_x * self.fir_weights.unsqueeze(0), dim=1)
        
        # Process through neural network
        out = self.relu(self.fc1(fir_output))
        out = self.dropout(out)
        out = self.relu(self.fc2(out))
        out = self.dropout(out)
        out = self.fc3(out)
        
        return out

class ElmanRNN(nn.Module):
    """Elman Recurrent Neural Network for full sequence modeling."""
    
    def __init__(self, input_size: int, hidden_size: int, output_size: int, num_layers: int = 2):
        super(ElmanRNN, self).__init__()
        
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        # Elman RNN (simple RNN)
        self.rnn = nn.RNN(input_size, hidden_size, num_layers, batch_first=True, dropout=0.2)
        
        # Output layers
        self.fc1 = nn.Linear(hidden_size, hidden_size // 2)
        self.fc2 = nn.Linear(hidden_size // 2, output_size)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.2)
        
    def forward(self, x, hidden=None):
        # x shape: (batch_size, sequence_length, input_size)
        
        # RNN forward pass
        rnn_out, hidden = self.rnn(x, hidden)
        
        # Take the last output
        last_output = rnn_out[:, -1, :]
        
        # Process through fully connected layers
        out = self.relu(self.fc1(last_output))
        out = self.dropout(out)
        out = self.fc2(out)
        
        return out, hidden

class TwoStageEnsemble:
    """Two-stage ensemble system: Stage 1 (Concentration) → Stage 2 (Dosage)."""
    
    def __init__(self, demographic_size: int = 6, sequence_length: int = 7):
        self.demographic_size = demographic_size
        self.sequence_length = sequence_length
        
        # Stage 1: Predict blood concentration
        # Input: demographics + dose history + previous concentrations
        stage1_input_size = demographic_size + 2  # demographics + dose + prev_concentration
        
        self.stage1_mlp = MLPNetwork(
            input_size=stage1_input_size,
            hidden_sizes=[64, 32, 16],
            output_size=1
        )
        
        self.stage1_fir = FIRNeuralNetwork(
            input_size=stage1_input_size,
            fir_length=3,
            hidden_size=32,
            output_size=1
        )
        
        self.stage1_elman = ElmanRNN(
            input_size=stage1_input_size,
            hidden_size=32,
            output_size=1,
            num_layers=2
        )
        
        # Stage 2: Predict optimal dose
        # Input: demographics + predicted concentration + concentration history
        stage2_input_size = demographic_size + 2  # demographics + predicted_conc + target_conc
        
        self.stage2_mlp = MLPNetwork(
            input_size=stage2_input_size,
            hidden_sizes=[64, 32, 16],
            output_size=1
        )
        
        self.stage2_fir = FIRNeuralNetwork(
            input_size=stage2_input_size,
            fir_length=3,
            hidden_size=32,
            output_size=1
        )
        
        self.stage2_elman = ElmanRNN(
            input_size=stage2_input_size,
            hidden_size=32,
            output_size=1,
            num_layers=2
        )
        
        # Ensemble weights (learnable)
        self.stage1_weights = nn.Parameter(torch.tensor([0.33, 0.33, 0.34]))
        self.stage2_weights = nn.Parameter(torch.tensor([0.33, 0.33, 0.34]))
        
        # Optimizers
        self.stage1_optimizers = [
            optim.Adam(self.stage1_mlp.parameters(), lr=0.001),
            optim.Adam(self.stage1_fir.parameters(), lr=0.001),
            optim.Adam(self.stage1_elman.parameters(), lr=0.001)
        ]
        
        self.stage2_optimizers = [
            optim.Adam(self.stage2_mlp.parameters(), lr=0.001),
            optim.Adam(self.stage2_fir.parameters(), lr=0.001),
            optim.Adam(self.stage2_elman.parameters(), lr=0.001)
        ]
        
        self.ensemble_optimizer = optim.Adam([self.stage1_weights, self.stage2_weights], lr=0.01)
        
        self.criterion = nn.MSELoss()
        
    def prepare_stage1_input(self, patient_data: PatientTimeSeries) -> Tuple[torch.Tensor, torch.Tensor]:
        """Prepare input for Stage 1 (concentration prediction)."""
        batch_size = 1
        seq_len = len(patient_data.dose_history)
        
        # Create sequence input
        sequence_input = []
        for i in range(seq_len):
            # Combine demographics, dose, and previous concentration
            dose = patient_data.dose_history[i]
            prev_conc = patient_data.concentration_history[i-1] if i > 0 else 0.0
            
            input_vector = np.concatenate([
                patient_data.demographics,
                [dose, prev_conc]
            ])
            sequence_input.append(input_vector)
        
        # Convert to tensor
        sequence_tensor = torch.FloatTensor(sequence_input).unsqueeze(0)  # Add batch dimension
        
        # Static input for MLP (use last time point)
        static_input = torch.FloatTensor(sequence_input[-1]).unsqueeze(0)
        
        return static_input, sequence_tensor
    
    def prepare_stage2_input(self, patient_data: PatientTimeSeries, 
                           predicted_concentration: float, 
                           target_concentration: float = 250.0) -> Tuple[torch.Tensor, torch.Tensor]:
        """Prepare input for Stage 2 (dose prediction)."""
        
        # Create input combining demographics, predicted concentration, and target
        input_vector = np.concatenate([
            patient_data.demographics,
            [predicted_concentration, target_concentration]
        ])
        
        # For sequence models, create a sequence with concentration history
        sequence_input = []
        for i in range(len(patient_data.concentration_history)):
            conc = patient_data.concentration_history[i]
            seq_vector = np.concatenate([
                patient_data.demographics,
                [conc, target_concentration]
            ])
            sequence_input.append(seq_vector)
        
        # Add the predicted concentration as the next step
        sequence_input.append(input_vector)
        
        static_input = torch.FloatTensor(input_vector).unsqueeze(0)
        sequence_tensor = torch.FloatTensor(sequence_input).unsqueeze(0)
        
        return static_input, sequence_tensor
    
    def forward_stage1(self, static_input: torch.Tensor, sequence_input: torch.Tensor) -> torch.Tensor:
        """Forward pass through Stage 1 ensemble."""
        
        # Get predictions from each model
        mlp_pred = self.stage1_mlp(static_input)
        fir_pred = self.stage1_fir(sequence_input)
        elman_pred, _ = self.stage1_elman(sequence_input)
        
        # Ensemble combination
        weights = torch.softmax(self.stage1_weights, dim=0)
        ensemble_pred = (weights[0] * mlp_pred + 
                        weights[1] * fir_pred + 
                        weights[2] * elman_pred)
        
        return ensemble_pred, (mlp_pred, fir_pred, elman_pred)
    
    def forward_stage2(self, static_input: torch.Tensor, sequence_input: torch.Tensor) -> torch.Tensor:
        """Forward pass through Stage 2 ensemble."""
        
        # Get predictions from each model
        mlp_pred = self.stage2_mlp(static_input)
        fir_pred = self.stage2_fir(sequence_input)
        elman_pred, _ = self.stage2_elman(sequence_input)
        
        # Ensemble combination
        weights = torch.softmax(self.stage2_weights, dim=0)
        ensemble_pred = (weights[0] * mlp_pred + 
                        weights[1] * fir_pred + 
                        weights[2] * elman_pred)
        
        return ensemble_pred, (mlp_pred, fir_pred, elman_pred)
    
    def train_step(self, patient_data: PatientTimeSeries) -> Dict[str, float]:
        """Single training step for both stages."""
        
        # Stage 1: Predict concentration
        static1, sequence1 = self.prepare_stage1_input(patient_data)
        target_conc = torch.FloatTensor([[patient_data.target_concentration]])
        
        # Forward pass Stage 1
        pred_conc, stage1_individual = self.forward_stage1(static1, sequence1)
        stage1_loss = self.criterion(pred_conc, target_conc)
        
        # Backward pass Stage 1
        for optimizer in self.stage1_optimizers:
            optimizer.zero_grad()
        stage1_loss.backward(retain_graph=True)
        for optimizer in self.stage1_optimizers:
            optimizer.step()
        
        # Stage 2: Predict dose using predicted concentration
        predicted_conc_value = pred_conc.detach().item()
        static2, sequence2 = self.prepare_stage2_input(patient_data, predicted_conc_value)
        target_dose = torch.FloatTensor([[patient_data.target_dose]])
        
        # Forward pass Stage 2
        pred_dose, stage2_individual = self.forward_stage2(static2, sequence2)
        stage2_loss = self.criterion(pred_dose, target_dose)
        
        # Backward pass Stage 2
        for optimizer in self.stage2_optimizers:
            optimizer.zero_grad()
        stage2_loss.backward(retain_graph=True)
        for optimizer in self.stage2_optimizers:
            optimizer.step()
        
        # Update ensemble weights
        total_loss = stage1_loss + stage2_loss
        self.ensemble_optimizer.zero_grad()
        total_loss.backward()
        self.ensemble_optimizer.step()
        
        return {
            'stage1_loss': stage1_loss.item(),
            'stage2_loss': stage2_loss.item(),
            'total_loss': total_loss.item(),
            'predicted_concentration': predicted_conc_value,
            'predicted_dose': pred_dose.item()
        }
    
    def predict(self, patient_data: PatientTimeSeries, target_concentration: float = 250.0) -> Dict[str, float]:
        """Make prediction for new patient data."""
        
        with torch.no_grad():
            # Stage 1: Predict concentration
            static1, sequence1 = self.prepare_stage1_input(patient_data)
            pred_conc, stage1_individual = self.forward_stage1(static1, sequence1)
            
            # Stage 2: Predict dose
            predicted_conc_value = pred_conc.item()
            static2, sequence2 = self.prepare_stage2_input(patient_data, predicted_conc_value, target_concentration)
            pred_dose, stage2_individual = self.forward_stage2(static2, sequence2)
            
            return {
                'predicted_concentration': predicted_conc_value,
                'predicted_dose': pred_dose.item(),
                'stage1_individual': [p.item() for p in stage1_individual],
                'stage2_individual': [p.item() for p in stage2_individual],
                'stage1_weights': torch.softmax(self.stage1_weights, dim=0).tolist(),
                'stage2_weights': torch.softmax(self.stage2_weights, dim=0).tolist()
            }

def generate_synthetic_patient_data(n_patients: int = 20) -> List[PatientTimeSeries]:
    """Generate synthetic patient time series data."""
    patients = []
    
    for i in range(n_patients):
        # Demographics: [age, weight, sex, creatinine, liver_function, kidney_function]
        demographics = np.array([
            np.random.normal(50, 15),  # age
            np.random.normal(70, 15),  # weight
            np.random.choice([0, 1]),  # sex (0=F, 1=M)
            np.random.normal(1.2, 0.3),  # creatinine
            np.random.normal(1.0, 0.2),  # liver function
            np.random.normal(1.0, 0.2)   # kidney function
        ])
        
        # Generate 7-day history
        n_days = 7
        dose_history = []
        concentration_history = []
        time_points = []
        
        # Initial dose based on weight
        base_dose = 5.0 * demographics[1]  # 5 mg/kg
        
        for day in range(n_days):
            # Dose adjustment based on previous concentration
            if day == 0:
                dose = base_dose
            else:
                last_conc = concentration_history[-1]
                if last_conc < 150:  # Too low
                    dose = dose_history[-1] * 1.1
                elif last_conc > 350:  # Too high
                    dose = dose_history[-1] * 0.9
                else:
                    dose = dose_history[-1]
            
            dose_history.append(dose)
            
            # Simulate concentration with patient-specific pharmacokinetics
            clearance = 0.5 + 0.3 * (demographics[3] - 1.0)  # Creatinine effect
            volume = 0.7 * demographics[1]  # Weight-based volume
            
            # Simple PK model with noise
            concentration = dose / (clearance * volume) * np.random.normal(1.0, 0.15)
            concentration = max(0, concentration)
            
            concentration_history.append(concentration)
            time_points.append(day * 24)
        
        # Target for next day
        target_concentration = np.random.normal(250, 50)  # Target therapeutic level
        target_dose = base_dose * np.random.normal(1.0, 0.2)  # Realistic dose adjustment
        
        patient = PatientTimeSeries(
            patient_id=f"P{i+1:03d}",
            demographics=demographics,
            dose_history=np.array(dose_history),
            concentration_history=np.array(concentration_history),
            time_points=np.array(time_points),
            target_concentration=target_concentration,
            target_dose=target_dose
        )
        
        patients.append(patient)
    
    return patients

if __name__ == "__main__":
    print("Neural Network Architectures for Two-Stage Pharmaceutical Modeling")
    print("=" * 70)
    
    # Generate synthetic data
    patients = generate_synthetic_patient_data(20)
    print(f"Generated {len(patients)} synthetic patients")
    
    # Initialize ensemble
    ensemble = TwoStageEnsemble()
    print("Initialized two-stage ensemble with MLP, FIR, and Elman networks")
    
    # Training example
    print("\nTraining example on first patient:")
    patient = patients[0]
    result = ensemble.train_step(patient)
    
    print(f"Stage 1 Loss: {result['stage1_loss']:.4f}")
    print(f"Stage 2 Loss: {result['stage2_loss']:.4f}")
    print(f"Predicted Concentration: {result['predicted_concentration']:.2f} ng/mL")
    print(f"Predicted Dose: {result['predicted_dose']:.2f} mg")
    
    # Prediction example
    print("\nPrediction example:")
    prediction = ensemble.predict(patient, target_concentration=250.0)
    print(f"Target Concentration: 250.0 ng/mL")
    print(f"Predicted Concentration: {prediction['predicted_concentration']:.2f} ng/mL")
    print(f"Recommended Dose: {prediction['predicted_dose']:.2f} mg")
    print(f"Stage 1 Weights: {[f'{w:.3f}' for w in prediction['stage1_weights']]}")
    print(f"Stage 2 Weights: {[f'{w:.3f}' for w in prediction['stage2_weights']]}")
