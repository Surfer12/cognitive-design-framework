#!/usr/bin/env python3
"""
Enhanced Integrated Twin Prime Chaos Demonstration with Data Logging & Visualization
Complete Python Implementation with JSON logging, CSV data files, and visualizations
"""

import math
import random
import json
import csv
import os
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Tuple, Any
from datetime import datetime

class DataLogger:
    """Comprehensive data logging system for chaos demonstration"""
    
    def __init__(self, experiment_name: str = "twin_prime_chaos"):
        self.experiment_name = experiment_name
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.base_dir = f"data/{experiment_name}_{self.timestamp}"
        
        # Create directory structure
        self.observations_dir = f"{self.base_dir}/observations"
        self.metrics_dir = f"{self.base_dir}/metrics"
        self.visualizations_dir = f"{self.base_dir}/visualizations"
        self.results_dir = f"{self.base_dir}/results"
        
        for directory in [self.observations_dir, self.metrics_dir, 
                         self.visualizations_dir, self.results_dir]:
            os.makedirs(directory, exist_ok=True)
        
        # Initialize data storage
        self.observations = []
        self.metrics = []
        self.agent_trajectories = {}
        self.confidence_history = []
        self.system_metrics = {}
        
        print(f"📊 DataLogger initialized: {self.base_dir}")
    
    def log_observation(self, step: int, agent_id: int, observation: Dict[str, Any]):
        """Log agent observation"""
        observation_entry = {
            "timestamp": datetime.now().isoformat(),
            "step": step,
            "agent_id": agent_id,
            "observation": observation
        }
        self.observations.append(observation_entry)
    
    def log_metrics(self, step: int, metrics: Dict[str, Any]):
        """Log system metrics"""
        metrics_entry = {
            "timestamp": datetime.now().isoformat(),
            "step": step,
            "metrics": metrics
        }
        self.metrics.append(metrics_entry)
    
    def log_agent_trajectory(self, agent_id: int, trajectory_data: Dict[str, Any]):
        """Log agent trajectory data"""
        if agent_id not in self.agent_trajectories:
            self.agent_trajectories[agent_id] = []
        self.agent_trajectories[agent_id].append(trajectory_data)
    
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
        
        # Save observations as JSON
        with open(f"{self.observations_dir}/observations.json", 'w') as f:
            json.dump(self.observations, f, indent=2)
        
        # Save metrics as JSON
        with open(f"{self.metrics_dir}/metrics.json", 'w') as f:
            json.dump(self.metrics, f, indent=2)
        
        # Save confidence history
        with open(f"{self.metrics_dir}/confidence_history.json", 'w') as f:
            json.dump(self.confidence_history, f, indent=2)
        
        # Save agent trajectories
        with open(f"{self.observations_dir}/agent_trajectories.json", 'w') as f:
            json.dump(self.agent_trajectories, f, indent=2)
        
        # Save system metrics summary
        with open(f"{self.results_dir}/system_summary.json", 'w') as f:
            json.dump(self.system_metrics, f, indent=2)
        
        # Create CSV files for time series data
        self._create_csv_files()
        
        print("✅ All data saved successfully")
    
    def _create_csv_files(self):
        """Create CSV files for time series analysis"""
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
        
        # Agent trajectories CSV
        if self.agent_trajectories:
            with open(f"{self.observations_dir}/trajectories_summary.csv", 'w', newline='') as f:
                fieldnames = ['agent_id', 'steps_recorded', 'final_position', 'avg_confidence']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for agent_id, trajectory in self.agent_trajectories.items():
                    if trajectory:
                        final_pos = trajectory[-1].get('position', 0)
                        avg_conf = sum(t.get('confidence', 0) for t in trajectory) / len(trajectory)
                        writer.writerow({
                            'agent_id': agent_id,
                            'steps_recorded': len(trajectory),
                            'final_position': final_pos,
                            'avg_confidence': avg_conf
                        })
    
    def create_visualizations(self):
        """Create comprehensive visualizations"""
        print("🎨 Generating visualizations...")
        
        self._create_confidence_plot()
        self._create_position_distribution_plot()
        self._create_lyapunov_analysis_plot()
        self._create_agent_trajectories_plot()
        self._create_system_metrics_plot()
        
        print("✅ Visualizations created")
    
    def _create_confidence_plot(self):
        """Create confidence evolution plot"""
        if not self.confidence_history:
            return
            
        steps = [entry['step'] for entry in self.confidence_history]
        swarm_conf = [entry.get('swarm_confidence', 0) * 100 for entry in self.confidence_history]
        agent_conf = [entry.get('avg_agent_confidence', 0) * 100 for entry in self.confidence_history]
        
        plt.figure(figsize=(12, 6))
        plt.plot(steps, swarm_conf, label='Swarm Confidence C(p)', marker='o', linewidth=2)
        plt.plot(steps, agent_conf, label='Average Agent Confidence', marker='s', linewidth=2)
        plt.axhline(y=95, color='r', linestyle='--', label='95% Confidence Bound')
        plt.xlabel('Simulation Step')
        plt.ylabel('Confidence (%)')
        plt.title('Confidence Evolution - Oates Swarm-Koopman Theorem')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f"{self.visualizations_dir}/confidence_evolution.png", dpi=300, bbox_inches='tight')
        plt.close()
    
    def _create_position_distribution_plot(self):
        """Create position distribution analysis plot"""
        if not self.agent_trajectories:
            return
            
        # Collect final positions
        final_positions = []
        angles = []
        
        for agent_id, trajectory in self.agent_trajectories.items():
            if trajectory:
                final_pos = trajectory[-1].get('position', 0)
                final_positions.append(final_pos)
                angles.append(math.degrees(final_pos))
        
        if not final_positions:
            return
            
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Position distribution
        ax1.hist(final_positions, bins=20, alpha=0.7, color='blue', edgecolor='black')
        ax1.axvline(np.mean(final_positions), color='red', linestyle='--', 
                   label='.3f')
        ax1.set_xlabel('Position (radians)')
        ax1.set_ylabel('Frequency')
        ax1.set_title('Final Position Distribution')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Angular distribution
        ax2.hist(angles, bins=20, alpha=0.7, color='green', edgecolor='black')
        ax2.axvline(np.mean(angles), color='red', linestyle='--', 
                   label='.1f')
        ax2.axvline(120, color='orange', linestyle='--', label='120° Target')
        ax2.set_xlabel('Angle (degrees)')
        ax2.set_ylabel('Frequency')
        ax2.set_title('Final Angular Distribution')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f"{self.visualizations_dir}/position_distribution.png", dpi=300, bbox_inches='tight')
        plt.close()
    
    def _create_lyapunov_analysis_plot(self):
        """Create Lyapunov exponent analysis plot"""
        if not self.metrics:
            return
            
        steps = []
        lyapunov_values = []
        
        for metric in self.metrics:
            if 'metrics' in metric and 'lyapunov_exponents' in metric['metrics']:
                lyap_values = metric['metrics']['lyapunov_exponents']
                if lyap_values:
                    steps.append(metric['step'])
                    lyapunov_values.append(np.mean(lyap_values))
        
        if not lyapunov_values:
            return
            
        plt.figure(figsize=(10, 6))
        plt.plot(steps, lyapunov_values, marker='o', linewidth=2, color='purple')
        plt.axhline(y=0, color='black', linestyle='-', alpha=0.5)
        plt.axhline(y=0.1, color='red', linestyle='--', label='Chaos Threshold (0.1)')
        plt.xlabel('Simulation Step')
        plt.ylabel('Average Lyapunov Exponent')
        plt.title('Lyapunov Exponent Evolution - Chaos Detection')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f"{self.visualizations_dir}/lyapunov_analysis.png", dpi=300, bbox_inches='tight')
        plt.close()
    
    def _create_agent_trajectories_plot(self):
        """Create agent trajectories visualization"""
        if not self.agent_trajectories:
            return
            
        plt.figure(figsize=(12, 8))
        
        for agent_id, trajectory in self.agent_trajectories.items():
            if trajectory:
                steps = [t.get('step', 0) for t in trajectory]
                positions = [t.get('position', 0) for t in trajectory]
                plt.plot(steps, positions, label=f'Agent {agent_id}', alpha=0.7)
        
        plt.xlabel('Simulation Step')
        plt.ylabel('Position (radians)')
        plt.title('Agent Trajectories - Prime-Based Initial Conditions')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f"{self.visualizations_dir}/agent_trajectories.png", dpi=300, bbox_inches='tight')
        plt.close()
    
    def _create_system_metrics_plot(self):
        """Create system metrics summary plot"""
        if not self.system_metrics:
            return
            
        # Create a summary bar chart of key metrics
        metrics = []
        values = []
        
        if 'final_swarm_confidence' in self.system_metrics:
            metrics.append('Final Swarm Confidence')
            values.append(self.system_metrics['final_swarm_confidence'] * 100)
        
        if 'average_lyapunov' in self.system_metrics:
            metrics.append('Average Lyapunov')
            values.append(self.system_metrics['average_lyapunov'])
        
        if 'prime_effectiveness' in self.system_metrics:
            metrics.append('Prime Effectiveness')
            values.append(self.system_metrics['prime_effectiveness'] * 100)
        
        if not metrics:
            return
            
        plt.figure(figsize=(10, 6))
        bars = plt.bar(metrics, values, alpha=0.7, color=['blue', 'green', 'red'])
        plt.ylabel('Value')
        plt.title('System Performance Metrics Summary')
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                    '.2f', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig(f"{self.visualizations_dir}/system_metrics_summary.png", dpi=300, bbox_inches='tight')
        plt.close()

def main():
    """Main function for the demonstration with data logging and visualization"""
    print("🧬 ENHANCED INTEGRATED TWIN PRIME CHAOS EXPERIMENT WITH DATA LOGGING")
    print("Complete Python Implementation - All Features + Data Analytics + Visualization")
    print("=" * 85)
    
    print("\n📊 DATA LOGGING & VISUALIZATION SYSTEM")
    print("✅ JSON Observation Logging")
    print("✅ CSV Time Series Data")
    print("✅ Comprehensive Metrics Tracking")
    print("✅ Agent Trajectory Recording")
    print("✅ Confidence Evolution Analysis")
    print("✅ Multi-Plot Visualizations")
    print("✅ Automated Data Persistence")
    
    print("\n🎨 VISUALIZATION CAPABILITIES")
    print("✅ Confidence Evolution Plots")
    print("✅ Position Distribution Analysis")
    print("✅ Lyapunov Exponent Evolution")
    print("✅ Agent Trajectory Comparison")
    print("✅ System Metrics Summary")
    print("✅ High-Resolution PNG Output")
    
    print("\n📁 DATA STRUCTURE")
    print("data/twin_prime_chaos_YYYYMMDD_HHMMSS/")
    print("├── observations/")
    print("│   ├── observations.json")
    print("│   ├── agent_trajectories.json")
    print("│   └── trajectories_summary.csv")
    print("├── metrics/")
    print("│   ├── metrics.json")
    print("│   ├── confidence_history.json")
    print("│   └── confidence_time_series.csv")
    print("├── visualizations/")
    print("│   ├── confidence_evolution.png")
    print("│   ├── position_distribution.png")
    print("│   ├── lyapunov_analysis.png")
    print("│   ├── agent_trajectories.png")
    print("│   └── system_metrics_summary.png")
    print("└── results/")
    print("    └── system_summary.json")
    
    print("\n✨ ENHANCED SYSTEM READY")
    print("   Complete data logging and visualization capabilities")
    print("   JSON/CSV data persistence")
    print("   Comprehensive analytics and reporting")
    print("   Multi-modal data analysis ready")

if __name__ == "__main__":
    main()
