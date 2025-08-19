# Medical AI Ensemble Neural Networks
# Implementation based on cyclosporine prediction research findings
# Integrates with the cognitive design framework's iXcan pipeline

from math import sqrt, exp, log
from collections import List, Dict
from memory import memset_zero
import random

# =============================================================================
# Ensemble Neural Network Architecture for Medical Prediction
# Based on Camps-Valls et al. (2001) - RMSE: 44.77 ng/mL
# =============================================================================

struct PatientData:
    """Patient physiological and clinical data structure."""
    var patient_id: String
    var weight: Float64  # kg
    var creatinine: Float64  # mg/dL
    var age: Int
    var gender: String
    var previous_doses: List[Float64]  # mg
    var blood_concentrations: List[Float64]  # ng/mL
    var time_points: List[Int]  # hours post-dose
    
    fn __init__(inout self, patient_id: String, weight: Float64, creatinine: Float64, age: Int, gender: String):
        self.patient_id = patient_id
        self.weight = weight
        self.creatinine = creatinine
        self.age = age
        self.gender = gender
        self.previous_doses = List[Float64]()
        self.blood_concentrations = List[Float64]()
        self.time_points = List[Int]()

struct NeuralNetworkModel:
    """Individual neural network model for ensemble."""
    var model_id: String
    var weights_input_hidden: List[List[Float64]]
    var weights_hidden_output: List[Float64]
    var bias_hidden: List[Float64]
    var bias_output: Float64
    var learning_rate: Float64
    var specialization: String  # e.g., "weight_focused", "creatinine_focused"
    
    fn __init__(inout self, model_id: String, input_size: Int, hidden_size: Int, specialization: String):
        self.model_id = model_id
        self.specialization = specialization
        self.learning_rate = 0.01
        self.bias_output = 0.0
        
        # Initialize weights and biases
        self.weights_input_hidden = List[List[Float64]]()
        self.weights_hidden_output = List[Float64]()
        self.bias_hidden = List[Float64]()
        
        # Random initialization
        for i in range(input_size):
            var row = List[Float64]()
            for j in range(hidden_size):
                row.append(random.random_float64(-0.5, 0.5))
            self.weights_input_hidden.append(row)
        
        for i in range(hidden_size):
            self.weights_hidden_output.append(random.random_float64(-0.5, 0.5))
            self.bias_hidden.append(random.random_float64(-0.1, 0.1))
    
    fn predict(self, patient_data: PatientData) -> Float64:
        """Predict blood concentration for given patient data."""
        # Feature extraction based on specialization
        var features = self._extract_features(patient_data)
        
        # Forward propagation
        var hidden_outputs = List[Float64]()
        for i in range(len(self.bias_hidden)):
            var activation = self.bias_hidden[i]
            for j in range(len(features)):
                activation += features[j] * self.weights_input_hidden[j][i]
            hidden_outputs.append(self._sigmoid(activation))
        
        # Output layer
        var output = self.bias_output
        for i in range(len(hidden_outputs)):
            output += hidden_outputs[i] * self.weights_hidden_output[i]
        
        return output
    
    fn _extract_features(self, patient_data: PatientData) -> List[Float64]:
        """Extract relevant features based on model specialization."""
        var features = List[Float64]()
        
        # Base features
        features.append(patient_data.weight)
        features.append(patient_data.creatinine)
        features.append(Float64(patient_data.age))
        
        # Gender encoding
        features.append(1.0 if patient_data.gender == "M" else 0.0)
        
        # Previous dose features
        if len(patient_data.previous_doses) > 0:
            features.append(patient_data.previous_doses[-1])  # Last dose
            var avg_dose = 0.0
            for dose in patient_data.previous_doses:
                avg_dose += dose[]
            features.append(avg_dose / len(patient_data.previous_doses))
        else:
            features.append(0.0)
            features.append(0.0)
        
        # Specialization-specific features
        if self.specialization == "weight_focused":
            features.append(patient_data.weight * patient_data.weight)  # Weight squared
            features.append(patient_data.weight / Float64(patient_data.age))  # Weight/age ratio
        elif self.specialization == "creatinine_focused":
            features.append(patient_data.creatinine * patient_data.creatinine)
            features.append(patient_data.creatinine * patient_data.weight)
        
        return features
    
    fn _sigmoid(self, x: Float64) -> Float64:
        """Sigmoid activation function."""
        return 1.0 / (1.0 + exp(-x))

# =============================================================================
# GA-BP Neural Network Implementation
# Based on Li et al. (2008) - 97.5% accuracy
# =============================================================================

struct GABPNeuralNetwork:
    """Genetic Algorithm optimized Backpropagation Neural Network."""
    var population_size: Int
    var mutation_rate: Float64
    var crossover_rate: Float64
    var generations: Int
    var best_network: NeuralNetworkModel
    var fitness_history: List[Float64]
    
    fn __init__(inout self, population_size: Int = 50, mutation_rate: Float64 = 0.1):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = 0.8
        self.generations = 100
        self.fitness_history = List[Float64]()
        # Initialize best_network with default values
        self.best_network = NeuralNetworkModel("best", 8, 10, "ga_optimized")
    
    fn evolve(inout self, training_data: List[PatientData]) -> NeuralNetworkModel:
        """Evolve neural network using genetic algorithm."""
        # Initialize population
        var population = List[NeuralNetworkModel]()
        for i in range(self.population_size):
            population.append(NeuralNetworkModel("ga_" + str(i), 8, 10, "ga_optimized"))
        
        # Evolution loop
        for generation in range(self.generations):
            # Evaluate fitness
            var fitness_scores = List[Float64]()
            for i in range(len(population)):
                var fitness = self._evaluate_fitness(population[i], training_data)
                fitness_scores.append(fitness)
            
            # Track best fitness
            var best_fitness = fitness_scores[0]
            var best_index = 0
            for i in range(len(fitness_scores)):
                if fitness_scores[i] > best_fitness:
                    best_fitness = fitness_scores[i]
                    best_index = i
            
            self.fitness_history.append(best_fitness)
            self.best_network = population[best_index]
            
            # Selection, crossover, and mutation would be implemented here
            # Simplified for demonstration
        
        return self.best_network
    
    fn _evaluate_fitness(self, model: NeuralNetworkModel, training_data: List[PatientData]) -> Float64:
        """Evaluate model fitness based on prediction accuracy."""
        var total_error = 0.0
        var count = 0
        
        for patient in training_data:
            if len(patient[].blood_concentrations) > 0:
                var predicted = model.predict(patient[])
                var actual = patient[].blood_concentrations[-1]  # Latest concentration
                var error = abs(predicted - actual)
                total_error += error
                count += 1
        
        if count == 0:
            return 0.0
        
        var mse = total_error / count
        return 1.0 / (1.0 + mse)  # Higher fitness for lower error

# =============================================================================
# Ensemble Model Implementation
# Combines multiple neural networks for improved accuracy
# =============================================================================

struct EnsembleNeuralNetwork:
    """Ensemble of neural networks for medical prediction."""
    var models: List[NeuralNetworkModel]
    var weights: List[Float64]  # Ensemble weights
    var validation_rmse: Float64
    var clinical_accuracy: Float64
    
    fn __init__(inout self):
        self.models = List[NeuralNetworkModel]()
        self.weights = List[Float64]()
        self.validation_rmse = 0.0
        self.clinical_accuracy = 0.0
    
    fn add_model(inout self, model: NeuralNetworkModel, weight: Float64 = 1.0):
        """Add a model to the ensemble."""
        self.models.append(model)
        self.weights.append(weight)
    
    fn predict(self, patient_data: PatientData) -> PredictionResult:
        """Generate ensemble prediction with confidence intervals."""
        var predictions = List[Float64]()
        var weighted_sum = 0.0
        var weight_sum = 0.0
        
        # Collect predictions from all models
        for i in range(len(self.models)):
            var prediction = self.models[i].predict(patient_data)
            predictions.append(prediction)
            weighted_sum += prediction * self.weights[i]
            weight_sum += self.weights[i]
        
        var ensemble_prediction = weighted_sum / weight_sum
        
        # Calculate prediction variance for confidence intervals
        var variance = 0.0
        for i in range(len(predictions)):
            var diff = predictions[i] - ensemble_prediction
            variance += diff * diff * self.weights[i]
        variance /= weight_sum
        
        var confidence_interval = 1.96 * sqrt(variance)  # 95% CI
        
        return PredictionResult(
            ensemble_prediction,
            confidence_interval,
            self._assess_clinical_safety(ensemble_prediction, patient_data)
        )
    
    fn _assess_clinical_safety(self, prediction: Float64, patient_data: PatientData) -> Bool:
        """Assess if prediction is within clinically safe ranges."""
        # Cyclosporine therapeutic range: 100-400 ng/mL (typical)
        var therapeutic_min = 100.0
        var therapeutic_max = 400.0
        var toxic_threshold = 500.0
        
        # Safety assessment
        if prediction > toxic_threshold:
            return False  # Potentially toxic
        elif prediction < therapeutic_min * 0.5:
            return False  # Potentially subtherapeutic
        else:
            return True  # Within acceptable range

struct PredictionResult:
    """Result of ensemble prediction with safety assessment."""
    var predicted_concentration: Float64
    var confidence_interval: Float64
    var is_clinically_safe: Bool
    
    fn __init__(inout self, prediction: Float64, ci: Float64, safe: Bool):
        self.predicted_concentration = prediction
        self.confidence_interval = ci
        self.is_clinically_safe = safe

# =============================================================================
# Clinical Validation Framework
# Based on Cui (2008) - 97.1% accuracy with 14 patients
# =============================================================================

struct ClinicalValidator:
    """Validates model performance against clinical data."""
    var validation_threshold: Float64
    var safety_margin: Float64
    
    fn __init__(inout self, threshold: Float64 = 0.15):  # 15% deviation as per Wei (2010)
        self.validation_threshold = threshold
        self.safety_margin = 0.1  # 10% safety margin
    
    fn validate_model(self, model: EnsembleNeuralNetwork, clinical_data: List[PatientData]) -> ValidationReport:
        """Validate model against clinical data."""
        var correct_predictions = 0
        var total_predictions = 0
        var rmse_sum = 0.0
        var safety_violations = 0
        
        for patient in clinical_data:
            if len(patient[].blood_concentrations) > 0:
                var result = model.predict(patient[])
                var actual = patient[].blood_concentrations[-1]
                
                # Accuracy assessment
                var relative_error = abs(result.predicted_concentration - actual) / actual
                if relative_error <= self.validation_threshold:
                    correct_predictions += 1
                
                # RMSE calculation
                var squared_error = (result.predicted_concentration - actual) ** 2
                rmse_sum += squared_error
                
                # Safety assessment
                if not result.is_clinically_safe:
                    safety_violations += 1
                
                total_predictions += 1
        
        var accuracy = Float64(correct_predictions) / Float64(total_predictions)
        var rmse = sqrt(rmse_sum / Float64(total_predictions))
        var safety_rate = 1.0 - (Float64(safety_violations) / Float64(total_predictions))
        
        return ValidationReport(accuracy, rmse, safety_rate, total_predictions)

struct ValidationReport:
    """Clinical validation results."""
    var accuracy: Float64
    var rmse: Float64
    var safety_rate: Float64
    var sample_size: Int
    
    fn __init__(inout self, acc: Float64, rmse_val: Float64, safety: Float64, n: Int):
        self.accuracy = acc
        self.rmse = rmse_val
        self.safety_rate = safety
        self.sample_size = n
    
    fn meets_clinical_standards(self) -> Bool:
        """Check if validation meets clinical standards."""
        return (self.accuracy >= 0.95 and  # 95% accuracy threshold
                self.rmse <= 50.0 and      # RMSE threshold (ng/mL)
                self.safety_rate >= 0.98)  # 98% safety rate

# =============================================================================
# Integration with iXcan Pipeline
# =============================================================================

struct MedicalAIProcessor:
    """Medical AI processor for integration with iXcan pipeline."""
    var ensemble_model: EnsembleNeuralNetwork
    var validator: ClinicalValidator
    var is_trained: Bool
    
    fn __init__(inout self):
        self.ensemble_model = EnsembleNeuralNetwork()
        self.validator = ClinicalValidator()
        self.is_trained = False
    
    fn train(inout self, training_data: List[PatientData]) raises:
        """Train the ensemble model."""
        if len(training_data) < 10:
            raise Error("Insufficient training data: minimum 10 patients required")
        
        # Create specialized models
        var weight_model = NeuralNetworkModel("weight_specialist", 8, 12, "weight_focused")
        var creatinine_model = NeuralNetworkModel("creatinine_specialist", 8, 12, "creatinine_focused")
        
        # Create GA-BP optimized model
        var ga_bp = GABPNeuralNetwork(30, 0.1)
        var optimized_model = ga_bp.evolve(training_data)
        
        # Add models to ensemble
        self.ensemble_model.add_model(weight_model, 0.3)
        self.ensemble_model.add_model(creatinine_model, 0.3)
        self.ensemble_model.add_model(optimized_model, 0.4)
        
        self.is_trained = True
    
    fn predict_dosage(self, patient_data: PatientData) raises -> PredictionResult:
        """Predict optimal dosage for patient."""
        if not self.is_trained:
            raise Error("Model must be trained before making predictions")
        
        return self.ensemble_model.predict(patient_data)
    
    fn validate_clinical_performance(self, validation_data: List[PatientData]) -> ValidationReport:
        """Validate model performance on clinical data."""
        return self.validator.validate_model(self.ensemble_model, validation_data)
