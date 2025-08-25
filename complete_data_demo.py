#!/usr/bin/env python3
"""
Complete Data Logging & JSON Output Demonstration
Shows the full data logging system with JSON and CSV outputs
"""

import math
import json
import csv
import os
from typing import Dict, List, Tuple, Any
from datetime import datetime

class DataLogger:
    """Complete data logging system with JSON and CSV outputs"""
    
    def __init__(self, experiment_name: str = "data_demo"):
        self.experiment_name = experiment_name
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.base_dir = f"data/{experiment_name}_{self.timestamp}"
        
        # Create directory structure
        self.observations_dir = f"{self.base_dir}/observations"
        self.metrics_dir = f"{self.base_dir}/metrics"
        self.results_dir = f"{self.base_dir}/results"
        
        for directory in [self.observations_dir, self.metrics_dir, self.results_dir]:
            os.makedirs(directory, exist_ok=True)
        
        # Initialize data storage
        self.observations = []
        self.metrics = []
        self.confidence_history = []
        
        print(f"📊 DataLogger initialized: {self.base_dir}")
    
    def log_observation(self, step: int, agent_id: int, observation: Dict[str, Any]):
        """Log agent observation to JSON"""
        observation_entry = {
            "timestamp": datetime.now().isoformat(),
            "step": step,
            "agent_id": agent_id,
            "observation": observation
        }
        self.observations.append(observation_entry)
        
        # Also log to individual agent file
        agent_file = f"{self.observations_dir}/agent_{agent_id}_observations.json"
        with open(agent_file, 'a') as f:
            json.dump(observation_entry, f)
            f.write('\n')
    
    def log_metrics(self, step: int, metrics: Dict[str, Any]):
        """Log system metrics to JSON"""
        metrics_entry = {
            "timestamp": datetime.now().isoformat(),
            "step": step,
            "metrics": metrics
        }
        self.metrics.append(metrics_entry)
    
    def log_confidence(self, step: int, confidence_data: Dict[str, Any]):
        """Log confidence measures"""
        confidence_entry = {
            "step": step,
            "timestamp": datetime.now().isoformat(),
            **confidence_data
        }
        self.confidence_history.append(confidence_entry)
    
    def save_all_data(self):
        """Save all collected data to files"""
        print(f"💾 Saving data to {self.base_dir}")
        
        # Save complete observations as JSON
        with open(f"{self.observations_dir}/complete_observations.json", 'w') as f:
            json.dump(self.observations, f, indent=2)
        
        # Save metrics as JSON
        with open(f"{self.metrics_dir}/system_metrics.json", 'w') as f:
            json.dump(self.metrics, f, indent=2)
        
        # Save confidence history as JSON
        with open(f"{self.metrics_dir}/confidence_history.json", 'w') as f:
            json.dump(self.confidence_history, f, indent=2)
        
        # Create CSV files for data analysis
        self._create_csv_files()
        
        # Create summary report
        self._create_summary_report()
        
        print("✅ All data saved successfully")
        
    def _create_csv_files(self):
        """Create CSV files for time series analysis"""
        # Observations CSV
        if self.observations:
            with open(f"{self.observations_dir}/observations.csv", 'w', newline='') as f:
                fieldnames = ['timestamp', 'step', 'agent_id', 'observation_type', 'value']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for obs in self.observations:
                    obs_data = obs['observation']
                    for key, value in obs_data.items():
                        if isinstance(value, (int, float)):
                            writer.writerow({
                                'timestamp': obs['timestamp'],
                                'step': obs['step'],
                                'agent_id': obs['agent_id'],
                                'observation_type': key,
                                'value': value
                            })
        
        # Confidence history CSV
        if self.confidence_history:
            with open(f"{self.metrics_dir}/confidence_time_series.csv", 'w', newline='') as f:
                fieldnames = ['step', 'timestamp', 'swarm_confidence', 'avg_agent_confidence', 'error_bound']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for entry in self.confidence_history:
                    writer.writerow({
                        'step': entry['step'],
                        'timestamp': entry['timestamp'],
                        'swarm_confidence': entry.get('swarm_confidence', 0),
                        'avg_agent_confidence': entry.get('avg_agent_confidence', 0),
                        'error_bound': entry.get('error_bound', 0)
                    })
    
    def _create_summary_report(self):
        """Create a comprehensive summary report"""
        summary = {
            "experiment_name": self.experiment_name,
            "timestamp": self.timestamp,
            "data_directory": self.base_dir,
            "summary_stats": {
                "total_observations": len(self.observations),
                "total_metrics": len(self.metrics),
                "total_confidence_entries": len(self.confidence_history),
                "unique_agents": len(set(obs['agent_id'] for obs in self.observations if obs['agent_id'] != -1))
            },
            "data_files_created": [
                f"{self.observations_dir}/complete_observations.json",
                f"{self.observations_dir}/observations.csv",
                f"{self.metrics_dir}/system_metrics.json",
                f"{self.metrics_dir}/confidence_history.json",
                f"{self.metrics_dir}/confidence_time_series.csv"
            ]
        }
        
        with open(f"{self.results_dir}/experiment_summary.json", 'w') as f:
            json.dump(summary, f, indent=2)

def demonstrate_data_logging():
    """Demonstrate the complete data logging system"""
    print("🧬 COMPLETE DATA LOGGING & JSON OUTPUT DEMONSTRATION")
    print("=" * 65)
    
    # Initialize data logger
    data_logger = DataLogger("complete_data_demo")
    
    print("\n�� LOGGING VARIOUS TYPES OF DATA:")
    print("-" * 40)
    
    # Log prime pair observations
    prime_pairs = [(3, 5), (5, 7), (11, 13), (17, 19)]
    for i, (p1, p2) in enumerate(prime_pairs):
        observation = {
            "prime_pair": f"({p1},{p2})",
            "ratio": p2 / p1,
            "difference": p2 - p1,
            "position_lower": 2.0944 + (p1 % 10) * 0.01,
            "position_upper": 2.0944 + (p2 % 10) * 0.01,
            "angle_lower_deg": math.degrees(2.0944 + (p1 % 10) * 0.01),
            "angle_upper_deg": math.degrees(2.0944 + (p2 % 10) * 0.01)
        }
        data_logger.log_observation(0, -1, observation)
        print(f"  Logged prime pair ({p1},{p2}) → {observation['angle_lower_deg']:.1f}° / {observation['angle_upper_deg']:.1f}°")
    
    # Log agent observations
    print("\n🎯 LOGGING AGENT OBSERVATIONS:")
    print("-" * 35)
    
    for step in range(5):
        for agent_id in range(4):
            observation = {
                "position": 2.0 + agent_id * 0.1 + step * 0.01,
                "velocity": 0.001 + agent_id * 0.0001,
                "confidence": max(0.1, 1.0 - step * 0.2),
                "energy": 0.5 * (0.001 + agent_id * 0.0001) ** 2,
                "chaos_measure": step * 0.1 + agent_id * 0.05
            }
            data_logger.log_observation(step, agent_id, observation)
            
            if step == 0:
                print(f"  Agent {agent_id}: Position = {observation['position']:.4f}, Confidence = {observation['confidence']:.2f}")
    
    # Log system metrics
    print("\n📈 LOGGING SYSTEM METRICS:")
    print("-" * 30)
    
    for step in range(5):
        metrics = {
            "step": step,
            "average_confidence": 1.0 - step * 0.15,
            "system_energy": 2.0 + step * 0.1,
            "chaos_level": step * 0.2,
            "prediction_accuracy": max(0.1, 1.0 - step * 0.2),
            "lyapunov_exponent": 0.1 + step * 0.05
        }
        data_logger.log_metrics(step, metrics)
        
        if step == 0:
            print(f"  Step {step}: Confidence = {metrics['average_confidence']:.2f}, Accuracy = {metrics['prediction_accuracy']:.2f}")
    
    # Log confidence evolution
    print("\n🎯 LOGGING CONFIDENCE EVOLUTION:")
    print("-" * 35)
    
    for step in range(10):
        confidence_data = {
            "swarm_confidence": max(0.0, 1.0 - step * 0.08),
            "avg_agent_confidence": max(0.0, 1.0 - step * 0.1),
            "error_bound": 0.01 + step * 0.002,
            "convergence_rate": 1.0 - step * 0.05,
            "theorem_validation": "C(p) ≥ 1 - ε" if step < 8 else "Theorem bounds satisfied"
        }
        data_logger.log_confidence(step, confidence_data)
        
        if step in [0, 5, 9]:
            print(f"  Step {step}: Swarm Confidence = {confidence_data['swarm_confidence']*100:.1f}%")
    
    # Save all data
    print("\n💾 SAVING ALL DATA:")
    print("-" * 25)
    data_logger.save_all_data()
    
    # Show data structure
    print("\n📂 COMPLETE DATA STRUCTURE CREATED:")
    print(f"├── {data_logger.observations_dir}/")
    print("│   ├── complete_observations.json")
    print("│   ├── observations.csv")
    print("│   └── agent_[id]_observations.json")
    print(f"├── {data_logger.metrics_dir}/")
    print("│   ├── system_metrics.json")
    print("│   ├── confidence_history.json")
    print("│   └── confidence_time_series.csv")
    print(f"└── {data_logger.results_dir}/")
    print("    └── experiment_summary.json")
    
    # Show sample data
    print("\n📊 SAMPLE DATA PREVIEW:")
    print("-" * 30)
    
    if data_logger.observations:
        sample_obs = data_logger.observations[0]
        print(f"Sample Observation: {sample_obs['observation']['prime_pair']}")
        print(f"  Ratio: {sample_obs['observation']['ratio']:.3f}")
        print(f"  Timestamp: {sample_obs['timestamp']}")
    
    if data_logger.confidence_history:
        sample_conf = data_logger.confidence_history[0]
        print(f"Sample Confidence: {sample_conf['swarm_confidence']*100:.1f}%")
    
    print("\n✨ COMPLETE DATA LOGGING DEMONSTRATION FINISHED")
    print("✅ JSON files created for all data types")
    print("✅ CSV files created for time series analysis")
    print("✅ Hierarchical data structure implemented")
    print("✅ Comprehensive data logging system validated")

def show_data_examples():
    """Show examples of the JSON data structure"""
    print("\n📋 JSON DATA STRUCTURE EXAMPLES:")
    print("=" * 40)
    
    print("\n🔢 OBSERVATION JSON STRUCTURE:")
    print('''{
  "timestamp": "2025-08-24T15:30:00.123456",
  "step": 0,
  "agent_id": 0,
  "observation": {
    "position": 2.1054,
    "velocity": 0.0012,
    "confidence": 0.95,
    "energy": 0.00000072,
    "chaos_measure": 0.15
  }
}''')
    
    print("\n📊 METRICS JSON STRUCTURE:")
    print('''{
  "timestamp": "2025-08-24T15:30:00.123456",
  "step": 2,
  "metrics": {
    "average_confidence": 0.85,
    "system_energy": 2.2,
    "chaos_level": 0.4,
    "prediction_accuracy": 0.8,
    "lyapunov_exponent": 0.25
  }
}''')
    
    print("\n🎯 CONFIDENCE JSON STRUCTURE:")
    print('''{
  "step": 5,
  "timestamp": "2025-08-24T15:30:00.123456",
  "swarm_confidence": 0.6,
  "avg_agent_confidence": 0.55,
  "error_bound": 0.02,
  "convergence_rate": 0.75,
  "theorem_validation": "C(p) ≥ 1 - ε"
}''')

def main():
    """Main demonstration function"""
    demonstrate_data_logging()
    show_data_examples()

if __name__ == "__main__":
    main()
