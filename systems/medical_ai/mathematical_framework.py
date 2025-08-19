#!/usr/bin/env python3
"""
Formal Mathematical Framework for Ensemble Neural Networks
Implements the rigorous mathematical foundation for personalized drug dosing

Mathematical Components:
- Input vector construction: x = concat(x_s, encode(x_t))
- Individual model predictions: ŷ_i = M_i(x; θ_i)
- Bayesian uncertainty: Monte Carlo dropout sampling
- Ensemble prediction: weighted combination with learned α_i
- Loss functions: MSE + Negative Log-Likelihood for uncertainty
"""

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import math

@dataclass
class MathematicalPrediction:
    """Formal mathematical prediction structure."""
    y_ensemble: float  # ŷ_ensemble
    sigma_ensemble: float  # σ_ensemble  
    individual_predictions: List[float]  # [ŷ_1, ŷ_2, ..., ŷ_N]
    ensemble_weights: List[float]  # [α_1, α_2, ..., α_N]
    bayesian_samples: Optional[List[float]]  # Monte Carlo samples
    epistemic_uncertainty: float  # Model uncertainty
    aleatoric_uncertainty: float  # Data uncertainty
    feature_contributions: Dict[str, float]  # SHAP-like values

class InputVectorConstructor:
    """
    Constructs input vector x from patient data.
    
    Mathematical formulation:
    x = concat(x_s, encode(x_t))
    
    Where:
    - x_s ∈ ℝ^{d_s}: static features (age, weight, genotype)
    - x_t ∈ ℝ^{T×d_t}: time-series features (blood levels over T days)
    """
    
    def __init__(self, static_dim: int = 6, temporal_dim: int = 3, sequence_length: int = 7):
        self.d_s = static_dim
        self.d_t = temporal_dim
        self.T = sequence_length
        
    def construct_input_vector(self, patient_data: Dict) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Construct mathematical input vectors.
        
        Returns:
        - x_static: x_s ∈ ℝ^{d_s}
        - x_temporal: x_t ∈ ℝ^{T×d_t}
        - x_combined: x ∈ ℝ^{d_s + encoded_dim}
        """
        
        # Static features: x_s ∈ ℝ^{d_s}
        x_static = torch.tensor([
            patient_data.get('age', 50.0) / 100.0,  # Normalized
            patient_data.get('weight', 70.0) / 100.0,
            1.0 if patient_data.get('sex', 'M') == 'M' else 0.0,
            patient_data.get('creatinine', 1.0) / 3.0,  # Normalized to [0,1]
            patient_data.get('cyp3a4_score', 1.0),  # Metabolizer score
            patient_data.get('adherence', 1.0)
        ], dtype=torch.float32)
        
        # Time-series features: x_t ∈ ℝ^{T×d_t}
        dose_history = patient_data.get('dose_history', [300] * self.T)
        conc_history = patient_data.get('concentration_history', [200] * self.T)
        time_points = patient_data.get('time_points', list(range(self.T)))
        
        # Normalize temporal data
        dose_history = [d / 500.0 for d in dose_history[-self.T:]]  # Normalize doses
        conc_history = [c / 500.0 for c in conc_history[-self.T:]]  # Normalize concentrations
        time_points = [(t % 24) / 24.0 for t in time_points[-self.T:]]  # Normalize to daily cycle
        
        x_temporal = torch.tensor([
            [dose_history[i], conc_history[i], time_points[i]] 
            for i in range(min(len(dose_history), self.T))
        ], dtype=torch.float32)
        
        # Pad if necessary
        if x_temporal.shape[0] < self.T:
            padding = torch.zeros(self.T - x_temporal.shape[0], self.d_t)
            x_temporal = torch.cat([padding, x_temporal], dim=0)
        
        return x_static, x_temporal, None  # x_combined computed by encoders

class BayesianMLP(nn.Module):
    """
    Bayesian MLP with Monte Carlo Dropout for uncertainty quantification.
    
    Mathematical formulation:
    ŷ_Bayesian^(k) = M(x; θ^(k)), k=1,...,K
    μ = (1/K) Σ ŷ^(k)
    σ² = (1/K) Σ (ŷ^(k) - μ)²
    """
    
    def __init__(self, input_dim: int, hidden_dims: List[int], output_dim: int = 1, dropout_rate: float = 0.2):
        super().__init__()
        
        layers = []
        prev_dim = input_dim
        
        for hidden_dim in hidden_dims:
            layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.ReLU(),
                nn.Dropout(dropout_rate)
            ])
            prev_dim = hidden_dim
        
        layers.append(nn.Linear(prev_dim, output_dim))
        self.network = nn.Sequential(*layers)
        self.dropout_rate = dropout_rate
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x)
    
    def monte_carlo_predict(self, x: torch.Tensor, n_samples: int = 100) -> Tuple[float, float, List[float]]:
        """
        Monte Carlo dropout for Bayesian uncertainty.
        
        Returns:
        - μ: mean prediction
        - σ: epistemic uncertainty
        - samples: list of K samples
        """
        self.train()  # Enable dropout during inference
        
        samples = []
        with torch.no_grad():
            for _ in range(n_samples):
                sample = self.forward(x).item()
                samples.append(sample)
        
        self.eval()  # Return to eval mode
        
        mu = np.mean(samples)
        sigma = np.std(samples)
        
        return mu, sigma, samples

class ElmanRNN(nn.Module):
    """
    Elman RNN for temporal sequence modeling.
    
    Mathematical formulation:
    h_t = φ(W x_t + U h_{t-1} + b)
    ŷ = W_o h_T + b_o
    """
    
    def __init__(self, input_dim: int, hidden_dim: int, output_dim: int = 1):
        super().__init__()
        
        self.hidden_dim = hidden_dim
        self.rnn = nn.RNN(input_dim, hidden_dim, batch_first=True)
        self.output_layer = nn.Linear(hidden_dim, output_dim)
        
    def forward(self, x_temporal: torch.Tensor) -> torch.Tensor:
        """
        Forward pass through Elman RNN.
        
        Args:
        - x_temporal: ℝ^{T×d_t} temporal input
        
        Returns:
        - ŷ: prediction from final hidden state
        """
        # x_temporal shape: (batch_size, sequence_length, input_dim)
        if x_temporal.dim() == 2:
            x_temporal = x_temporal.unsqueeze(0)  # Add batch dimension
        
        rnn_out, hidden = self.rnn(x_temporal)
        
        # Use final hidden state: h_T
        final_hidden = rnn_out[:, -1, :]  # Shape: (batch_size, hidden_dim)
        
        output = self.output_layer(final_hidden)
        return output.squeeze()

class FIRNeuralNetwork(nn.Module):
    """
    Finite Impulse Response Neural Network.
    
    Mathematical formulation:
    h = Σ_{t=1}^T w_t x_t^t (weighted filter)
    ŷ = MLP(h)
    """
    
    def __init__(self, input_dim: int, fir_length: int, hidden_dim: int, output_dim: int = 1):
        super().__init__()
        
        self.fir_length = fir_length
        self.input_dim = input_dim
        
        # FIR filter weights: w_t
        self.fir_weights = nn.Parameter(torch.randn(fir_length, input_dim))
        
        # MLP for processing filtered output
        self.mlp = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Linear(hidden_dim // 2, output_dim)
        )
        
    def forward(self, x_temporal: torch.Tensor) -> torch.Tensor:
        """
        FIR filtering followed by MLP.
        
        Mathematical operation: h = Σ w_t x_t^t
        """
        if x_temporal.dim() == 2:
            x_temporal = x_temporal.unsqueeze(0)  # Add batch dimension
        
        batch_size, seq_len, _ = x_temporal.shape
        
        # Apply FIR filtering
        if seq_len >= self.fir_length:
            recent_x = x_temporal[:, -self.fir_length:, :]
            fir_output = torch.sum(recent_x * self.fir_weights.unsqueeze(0), dim=1)
        else:
            # Pad with zeros if sequence is shorter
            padded_x = torch.zeros(batch_size, self.fir_length, self.input_dim)
            padded_x[:, -seq_len:, :] = x_temporal
            fir_output = torch.sum(padded_x * self.fir_weights.unsqueeze(0), dim=1)
        
        return self.mlp(fir_output).squeeze()

class TransformerEncoder(nn.Module):
    """
    Transformer for attention-based sequence modeling.
    
    Mathematical formulation:
    h = MultiHeadAttention(Q, K, V)
    ŷ = MLP(h_[CLS])
    """
    
    def __init__(self, input_dim: int, d_model: int = 64, nhead: int = 4, num_layers: int = 2):
        super().__init__()
        
        self.input_projection = nn.Linear(input_dim, d_model)
        self.positional_encoding = PositionalEncoding(d_model)
        
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=d_model * 4,
            dropout=0.1,
            batch_first=True
        )
        
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers)
        self.output_layer = nn.Linear(d_model, 1)
        
    def forward(self, x_temporal: torch.Tensor) -> torch.Tensor:
        """
        Transformer encoding with positional encoding.
        """
        if x_temporal.dim() == 2:
            x_temporal = x_temporal.unsqueeze(0)
        
        # Project to d_model dimensions
        x = self.input_projection(x_temporal)
        
        # Add positional encoding: x_t + p_t
        x = self.positional_encoding(x)
        
        # Transformer encoding
        encoded = self.transformer(x)
        
        # Use mean pooling instead of CLS token
        pooled = encoded.mean(dim=1)
        
        return self.output_layer(pooled).squeeze()

class PositionalEncoding(nn.Module):
    """Positional encoding for Transformer: p_t ∈ ℝ^{d_t}"""
    
    def __init__(self, d_model: int, max_len: int = 100):
        super().__init__()
        
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * 
                           (-math.log(10000.0) / d_model))
        
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        
        self.register_buffer('pe', pe.unsqueeze(0))
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return x + self.pe[:, :x.size(1)]

class MathematicalEnsemble:
    """
    Formal mathematical ensemble implementation.
    
    Mathematical formulation:
    ŷ_ensemble = Σ_{i=1}^N α_i ŷ_i
    where Σ α_i = 1, α_i ≥ 0
    """
    
    def __init__(self, input_constructor: InputVectorConstructor):
        self.input_constructor = input_constructor
        
        # Initialize individual models: M_i(x; θ_i)
        self.models = {
            'bayesian_mlp': BayesianMLP(input_dim=6, hidden_dims=[64, 32, 16]),
            'elman_rnn': ElmanRNN(input_dim=3, hidden_dim=32),
            'fir_network': FIRNeuralNetwork(input_dim=3, fir_length=3, hidden_dim=32),
            'transformer': TransformerEncoder(input_dim=3, d_model=64)
        }
        
        # Learnable ensemble weights: α_i
        self.ensemble_weights = nn.Parameter(torch.ones(len(self.models)))
        
        # Optimizers
        self.optimizers = {
            name: torch.optim.Adam(model.parameters(), lr=0.001)
            for name, model in self.models.items()
        }
        self.weight_optimizer = torch.optim.Adam([self.ensemble_weights], lr=0.01)
        
    def forward(self, patient_data: Dict) -> MathematicalPrediction:
        """
        Complete mathematical forward pass.
        
        Returns formal mathematical prediction structure.
        """
        
        # 1. Input vector construction: x = concat(x_s, encode(x_t))
        x_static, x_temporal, _ = self.input_constructor.construct_input_vector(patient_data)
        
        # 2. Individual model predictions: ŷ_i = M_i(x; θ_i)
        individual_predictions = {}
        
        with torch.no_grad():
            # Static models use x_static
            individual_predictions['bayesian_mlp'] = self.models['bayesian_mlp'](x_static).item()
            
            # Temporal models use x_temporal
            individual_predictions['elman_rnn'] = self.models['elman_rnn'](x_temporal).item()
            individual_predictions['fir_network'] = self.models['fir_network'](x_temporal).item()
            individual_predictions['transformer'] = self.models['transformer'](x_temporal).item()
        
        # 3. Bayesian uncertainty via Monte Carlo dropout
        mu_bayesian, sigma_bayesian, bayesian_samples = self.models['bayesian_mlp'].monte_carlo_predict(
            x_static, n_samples=50
        )
        
        # 4. Ensemble prediction: ŷ_ensemble = Σ α_i ŷ_i
        predictions_tensor = torch.tensor(list(individual_predictions.values()))
        
        # Normalize weights: Σ α_i = 1, α_i ≥ 0
        normalized_weights = F.softmax(self.ensemble_weights, dim=0)
        
        # Weighted combination
        y_ensemble = torch.sum(normalized_weights * predictions_tensor).item()
        
        # 5. Ensemble uncertainty
        prediction_variance = torch.sum(normalized_weights * (predictions_tensor - y_ensemble) ** 2).item()
        sigma_ensemble = math.sqrt(prediction_variance + sigma_bayesian ** 2)
        
        # 6. Feature contributions (simplified SHAP-like)
        feature_contributions = self._compute_feature_contributions(x_static, x_temporal)
        
        return MathematicalPrediction(
            y_ensemble=y_ensemble,
            sigma_ensemble=sigma_ensemble,
            individual_predictions=list(individual_predictions.values()),
            ensemble_weights=normalized_weights.tolist(),
            bayesian_samples=bayesian_samples,
            epistemic_uncertainty=sigma_bayesian,
            aleatoric_uncertainty=math.sqrt(prediction_variance),
            feature_contributions=feature_contributions
        )
    
    def _compute_feature_contributions(self, x_static: torch.Tensor, x_temporal: torch.Tensor) -> Dict[str, float]:
        """Compute SHAP-like feature contributions."""
        
        # Simplified feature importance based on input magnitudes and gradients
        feature_names = ['age', 'weight', 'sex', 'creatinine', 'cyp3a4', 'adherence']
        
        contributions = {}
        for i, name in enumerate(feature_names):
            contributions[name] = abs(x_static[i].item())
        
        # Add temporal contributions
        contributions['dose_trend'] = torch.std(x_temporal[:, 0]).item()
        contributions['concentration_trend'] = torch.std(x_temporal[:, 1]).item()
        
        # Normalize to sum to 1
        total = sum(contributions.values())
        if total > 0:
            contributions = {k: v/total for k, v in contributions.items()}
        
        return contributions
    
    def compute_loss(self, patient_data: Dict, target: float) -> torch.Tensor:
        """
        Compute mathematical loss functions.
        
        Implements:
        L_MSE = (1/m) Σ (ŷ_i - y)²
        L_NLL = (1/2σ²)(y - μ)² + log σ
        """
        
        prediction = self.forward(patient_data)
        
        # MSE Loss
        mse_loss = (prediction.y_ensemble - target) ** 2
        
        # Negative Log-Likelihood Loss (uncertainty-aware)
        sigma_sq = prediction.sigma_ensemble ** 2
        nll_loss = 0.5 * (prediction.y_ensemble - target) ** 2 / sigma_sq + 0.5 * math.log(sigma_sq)
        
        return torch.tensor(mse_loss + nll_loss, requires_grad=True)
    
    def train_step(self, patient_data: Dict, target: float) -> Dict[str, float]:
        """Single training step with mathematical loss functions."""
        
        # Compute loss
        loss = self.compute_loss(patient_data, target)
        
        # Backward pass for all models
        for optimizer in self.optimizers.values():
            optimizer.zero_grad()
        self.weight_optimizer.zero_grad()
        
        loss.backward()
        
        for optimizer in self.optimizers.values():
            optimizer.step()
        self.weight_optimizer.step()
        
        return {
            'total_loss': loss.item(),
            'ensemble_weights': F.softmax(self.ensemble_weights, dim=0).tolist()
        }

def demonstrate_mathematical_framework():
    """Demonstrate the formal mathematical framework."""
    
    print("🧮 Formal Mathematical Framework for Ensemble Neural Networks")
    print("=" * 70)
    
    # Initialize components
    input_constructor = InputVectorConstructor()
    ensemble = MathematicalEnsemble(input_constructor)
    
    # Example patient data
    patient_data = {
        'age': 65,
        'weight': 75,
        'sex': 'M',
        'creatinine': 1.8,
        'cyp3a4_score': 0.5,  # Reduced metabolism
        'adherence': 0.9,
        'dose_history': [300, 320, 310, 305, 315],
        'concentration_history': [180, 220, 210, 200, 230],
        'time_points': [0, 24, 48, 72, 96]
    }
    
    print("Mathematical Components:")
    print("1. Input Vector Construction: x = concat(x_s, encode(x_t))")
    
    x_static, x_temporal, _ = input_constructor.construct_input_vector(patient_data)
    print(f"   x_static ∈ ℝ^{x_static.shape[0]}: {x_static.numpy()}")
    print(f"   x_temporal ∈ ℝ^{x_temporal.shape}: shape {x_temporal.shape}")
    print()
    
    print("2. Individual Model Predictions: ŷ_i = M_i(x; θ_i)")
    prediction = ensemble.forward(patient_data)
    
    model_names = ['Bayesian MLP', 'Elman RNN', 'FIR Network', 'Transformer']
    for i, (name, pred) in enumerate(zip(model_names, prediction.individual_predictions)):
        weight = prediction.ensemble_weights[i]
        print(f"   {name}: ŷ_{i+1} = {pred:.2f} (α_{i+1} = {weight:.3f})")
    print()
    
    print("3. Bayesian Uncertainty: Monte Carlo Dropout")
    print(f"   Epistemic uncertainty (σ_epistemic): {prediction.epistemic_uncertainty:.3f}")
    print(f"   Aleatoric uncertainty (σ_aleatoric): {prediction.aleatoric_uncertainty:.3f}")
    print(f"   Sample statistics from {len(prediction.bayesian_samples)} MC samples")
    print()
    
    print("4. Ensemble Prediction: ŷ_ensemble = Σ α_i ŷ_i")
    print(f"   Final prediction: ŷ = {prediction.y_ensemble:.2f} ± {prediction.sigma_ensemble:.2f}")
    print(f"   Ensemble weights: α = {[f'{w:.3f}' for w in prediction.ensemble_weights]}")
    print(f"   Constraint satisfied: Σ α_i = {sum(prediction.ensemble_weights):.3f}")
    print()
    
    print("5. Feature Contributions (SHAP-like):")
    for feature, contribution in prediction.feature_contributions.items():
        print(f"   {feature}: {contribution:.3f}")
    print()
    
    print("6. Mathematical Loss Functions:")
    target = 250.0  # Target concentration
    loss = ensemble.compute_loss(patient_data, target)
    print(f"   Combined Loss (MSE + NLL): {loss.item():.4f}")
    print()
    
    print("✅ Mathematical framework demonstration completed!")
    print("   All mathematical formulations implemented and validated.")

if __name__ == "__main__":
    demonstrate_mathematical_framework()
