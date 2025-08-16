"""
Enhanced Analytic Number Theory Cognitive Demo
Integrates visualization and data storage with the cognitive framework
"""

import sys
import os
import time
from datetime import datetime, timezone
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

# Import visualization and storage tools
from tools.visualization.cognitive_plots import CognitiveVisualizer
from tools.storage.cognitive_data_manager import (
    CognitiveDataManager, CognitiveAnalysisResult, CognitiveDataAnalyzer
)

import numpy as np
import matplotlib.pyplot as plt
import json

class EnhancedCognitiveDemo:
    """Enhanced demo with full visualization and storage capabilities"""
    
    def __init__(self):
        self.visualizer = CognitiveVisualizer()
        self.data_manager = CognitiveDataManager()
        self.analyzer = CognitiveDataAnalyzer(self.data_manager)
        
        # Simulate the Mojo cognitive processor results
        # In real implementation, this would interface with the Mojo code
        self.session_id = self.data_manager.generate_session_id()
        
    def generate_cognitive_test_data(self, n_points: int = 200) -> list:
        """Generate test data representing cognitive inputs with various patterns"""
        data = []
        
        # Mix of rational and irrational cognitive patterns
        for i in range(n_points):
            t = i / n_points
            
            # Rational component (major arc behavior)
            rational_part = np.sin(2.0 * np.pi * t * 3.0)  # Period 1/3
            
            # Irrational component (minor arc behavior)  
            irrational_part = 0.3 * np.sin(2.0 * np.pi * t * np.sqrt(2))
            
            # Noise component
            noise = 0.1 * np.sin(2.0 * np.pi * t * 17.0)
            
            # Cognitive complexity measure
            complexity = rational_part + irrational_part + noise
            data.append(1.0 + 0.5 * complexity)  # Shift to avoid s=1 pole
        
        return data
    
    def simulate_circle_method_analysis(self, data: list) -> tuple:
        """Simulate circle method decomposition (would interface with Mojo code)"""
        arc_classifications = []
        contributions = []
        
        for value in data:
            # Simulate rational distance computation
            rational_distance = abs(value - round(value * 3) / 3)  # Distance to nearest 1/3
            
            is_major = rational_distance < 0.1  # Major arc threshold
            arc_classifications.append(is_major)
            
            if is_major:
                contribution = 1.0 / (1.0 + value * value)  # Rational weight
            else:
                contribution = (1.0 - np.exp(-value)) * 0.5  # Neural weight
            
            contributions.append(contribution)
        
        return arc_classifications, contributions
    
    def simulate_sieve_analysis(self, data: list) -> dict:
        """Simulate sieve theory analysis (would interface with Mojo code)"""
        # Simulate Selberg sieve filtering
        filtered_data = [x for x in data if abs(x - 1.0) > 0.05]  # Remove near-pole values
        
        # Simulate twin pair detection
        twin_pairs = []
        epsilon = 0.05
        for i in range(len(filtered_data) - 1):
            if abs(filtered_data[i+1] - filtered_data[i]) < epsilon:
                twin_pairs.append((filtered_data[i], filtered_data[i+1]))
        
        # Simulate prime patterns (first 20 primes)
        prime_patterns = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]
        
        return {
            'filtered_data': filtered_data,
            'twin_pairs': twin_pairs,
            'prime_patterns': prime_patterns,
            'dimension': len(filtered_data) ** 0.5
        }
    
    def simulate_laurent_analysis(self, data: list) -> dict:
        """Simulate Laurent expansion analysis (would interface with Mojo code)"""
        avg_input = np.mean(data)
        
        # Simulate cognitive zeta function values
        s_values = [0.9, 0.95, 0.99, 1.01, 1.05, 1.1]
        zeta_values = []
        local_richness = []
        
        for s in s_values:
            delta = s - 1.0
            
            # Simulate Laurent expansion: 1/(s-1) + γ + γ₁(s-1) + ...
            if abs(delta) > 1e-10:
                singular_part = 1.0 / delta
                regular_part = 0.5772 + (-0.0728) * delta  # Euler-Mascheroni + first Stieltjes
                zeta_val = singular_part + regular_part
            else:
                zeta_val = 1000.0  # Large value at pole
            
            zeta_values.append(zeta_val)
            
            # Local structure richness
            if abs(delta) > 1e-10:
                richness = abs(regular_part) / (abs(singular_part) + abs(regular_part))
            else:
                richness = 1.0
            
            local_richness.append(richness)
        
        return {
            's_values': s_values,
            'zeta_values': zeta_values,
            'local_richness': local_richness,
            'cognitive_zeta': zeta_values[3]  # Value at s=1.01
        }
    
    def simulate_gap_detection(self, filtered_data: list) -> list:
        """Simulate cognitive gap detection"""
        gaps = []
        threshold = 0.2
        
        sorted_data = sorted(filtered_data)
        for i in range(len(sorted_data) - 1):
            gap_size = sorted_data[i+1] - sorted_data[i]
            if gap_size > threshold:
                gaps.append((sorted_data[i], sorted_data[i+1]))
        
        return gaps
    
    def run_complete_analysis(self, save_results: bool = True, 
                            create_visualizations: bool = True) -> dict:
        """Run complete cognitive analysis with visualization and storage"""
        
        print("🧠 Enhanced Analytic Number Theory Cognitive Analysis")
        print("=" * 60)
        
        start_time = time.time()
        
        # Step 1: Generate test data
        print("1. Generating cognitive test data...")
        test_data = self.generate_cognitive_test_data(200)
        
        # Save raw data
        if save_results:
            raw_data_path = self.data_manager.save_raw_data(
                test_data, 
                {"description": "Enhanced demo test data", "n_points": len(test_data)},
                self.session_id
            )
        
        # Step 2: Circle method analysis
        print("2. Running circle method analysis...")
        arc_classifications, contributions = self.simulate_circle_method_analysis(test_data)
        
        major_count = sum(arc_classifications)
        minor_count = len(arc_classifications) - major_count
        major_avg = np.mean([c for c, is_major in zip(contributions, arc_classifications) if is_major]) if major_count > 0 else 0
        minor_avg = np.mean([c for c, is_major in zip(contributions, arc_classifications) if not is_major]) if minor_count > 0 else 0
        
        # Step 3: Sieve theory analysis
        print("3. Running sieve theory analysis...")
        sieve_results = self.simulate_sieve_analysis(test_data)
        
        # Step 4: Laurent expansion analysis
        print("4. Running Laurent expansion analysis...")
        laurent_results = self.simulate_laurent_analysis(test_data)
        
        # Step 5: Gap detection
        print("5. Detecting cognitive gaps...")
        gaps = self.simulate_gap_detection(sieve_results['filtered_data'])
        
        processing_time = (time.time() - start_time) * 1000
        
        # Compile results
        analysis_results = {
            'major_arc_average': major_avg,
            'minor_arc_average': minor_avg,
            'major_minor_ratio': major_count / max(minor_count, 1),
            'cognitive_zeta': laurent_results['cognitive_zeta'],
            'local_structure_richness': np.mean(laurent_results['local_richness']),
            'sieve_dimension': sieve_results['dimension'],
            'gaps_detected': len(gaps),
            'processing_time_ms': processing_time
        }
        
        # Create structured result object
        if save_results:
            structured_result = CognitiveAnalysisResult(
                timestamp=datetime.now(timezone.utc).isoformat(),
                session_id=self.session_id,
                input_data_hash=self.data_manager.compute_data_hash(test_data),
                major_arc_average=major_avg,
                minor_arc_average=minor_avg,
                major_minor_ratio=major_count / max(minor_count, 1),
                major_arc_count=major_count,
                minor_arc_count=minor_count,
                cognitive_zeta=laurent_results['cognitive_zeta'],
                local_structure_richness=np.mean(laurent_results['local_richness']),
                laurent_coefficients={-1: 1.0, 0: 0.5772, 1: -0.0728},
                sieve_dimension=sieve_results['dimension'],
                filtered_data_count=len(sieve_results['filtered_data']),
                original_data_count=len(test_data),
                twin_pairs_count=len(sieve_results['twin_pairs']),
                retention_rate=len(sieve_results['filtered_data']) / len(test_data),
                gaps_detected=len(gaps),
                average_gap_size=np.mean([g[1] - g[0] for g in gaps]) if gaps else 0,
                max_gap_size=max([g[1] - g[0] for g in gaps]) if gaps else 0,
                processing_time_ms=processing_time,
                framework_version="1.0.0",
                parameters={"arc_threshold": 0.1, "sieve_level": 100}
            )
            
            # Save structured result
            result_path = self.data_manager.save_analysis_result(structured_result, "enhanced_demo")
        
        # Create visualizations
        if create_visualizations:
            print("6. Creating visualizations...")
            
            vis_dir = self.data_manager.visualizations_path / f"session_{self.session_id}"
            vis_dir.mkdir(exist_ok=True)
            
            # Circle method plot
            self.visualizer.plot_circle_method_decomposition(
                test_data, arc_classifications, contributions,
                save_path=str(vis_dir / "circle_method_analysis.png")
            )
            
            # Sieve analysis plot
            self.visualizer.plot_sieve_analysis(
                test_data, sieve_results['filtered_data'], 
                sieve_results['twin_pairs'], sieve_results['prime_patterns'],
                save_path=str(vis_dir / "sieve_analysis.png")
            )
            
            # Laurent expansion plot
            self.visualizer.plot_laurent_expansion(
                laurent_results['s_values'], laurent_results['zeta_values'],
                laurent_results['local_richness'],
                save_path=str(vis_dir / "laurent_expansion.png")
            )
            
            # Cognitive gaps plot
            self.visualizer.plot_cognitive_gaps(
                sieve_results['filtered_data'], gaps,
                save_path=str(vis_dir / "cognitive_gaps.png")
            )
            
            # Integrated dashboard
            self.visualizer.plot_integrated_dashboard(
                analysis_results,
                save_path=str(vis_dir / "integrated_dashboard.png")
            )
        
        # Print summary
        print("\n" + "=" * 60)
        print("ANALYSIS COMPLETE")
        print("=" * 60)
        print(f"Session ID: {self.session_id}")
        print(f"Processing time: {processing_time:.2f} ms")
        print(f"Major/Minor ratio: {analysis_results['major_minor_ratio']:.4f}")
        print(f"Cognitive zeta: {analysis_results['cognitive_zeta']:.4f}")
        print(f"Local richness: {analysis_results['local_structure_richness']:.4f}")
        print(f"Sieve dimension: {analysis_results['sieve_dimension']:.4f}")
        print(f"Gaps detected: {analysis_results['gaps_detected']}")
        
        if save_results:
            print(f"\nResults saved to: {result_path}")
        
        if create_visualizations:
            print(f"Visualizations saved to: {vis_dir}")
        
        return analysis_results
    
    def demonstrate_data_management(self):
        """Demonstrate data management capabilities"""
        print("\n" + "=" * 60)
        print("DATA MANAGEMENT DEMONSTRATION")
        print("=" * 60)
        
        # List existing sessions
        sessions = self.data_manager.list_sessions()
        print(f"\nFound {len(sessions)} existing sessions:")
        
        for i, session in enumerate(sessions[:5]):  # Show first 5
            print(f"  {i+1}. {session['session_id']} - {session['timestamp'][:19]}")
            print(f"     Ratio: {session['major_minor_ratio']:.3f}, "
                  f"Zeta: {session['cognitive_zeta']:.3f}")
        
        if len(sessions) > 5:
            print(f"     ... and {len(sessions) - 5} more sessions")
        
        # Create summary if we have multiple sessions
        if len(sessions) >= 2:
            print("\n--- Session Summary Statistics ---")
            session_ids = [s['session_id'] for s in sessions[:10]]  # Analyze up to 10 sessions
            summary = self.data_manager.create_session_summary(session_ids)
            
            if 'statistics' in summary:
                stats = summary['statistics']
                print(f"Sessions analyzed: {summary['session_count']}")
                print(f"Major/Minor ratio - Mean: {stats['major_minor_ratio']['mean']:.4f}, "
                      f"Std: {stats['major_minor_ratio']['std']:.4f}")
                print(f"Cognitive zeta - Mean: {stats['cognitive_zeta']['mean']:.4f}, "
                      f"Std: {stats['cognitive_zeta']['std']:.4f}")
                
                if 'trends' in summary:
                    print("\n--- Trends ---")
                    for metric, trend in summary['trends'].items():
                        if 'direction' in trend:
                            print(f"{metric}: {trend['direction']} ({trend['magnitude']})")
        
        # Demonstrate anomaly detection
        if len(sessions) >= 10:
            print("\n--- Anomaly Detection ---")
            anomalies = self.analyzer.detect_anomalies(window_size=5)
            
            if anomalies:
                print(f"Found {len(anomalies)} anomalous sessions:")
                for anomaly in anomalies[:3]:  # Show top 3
                    print(f"  Session {anomaly['session_id']}: "
                          f"Max Z-score: {anomaly['max_z_score']:.2f}")
            else:
                print("No anomalies detected")
        
        # Export data
        if len(sessions) >= 2:
            print("\n--- Data Export ---")
            try:
                export_sessions = [s['session_id'] for s in sessions[:5]]
                csv_path = self.data_manager.export_to_csv(export_sessions)
                print(f"Exported {len(export_sessions)} sessions to CSV")
            except Exception as e:
                print(f"Export failed: {e}")

def main():
    """Run the enhanced demonstration"""
    demo = EnhancedCognitiveDemo()
    
    # Run complete analysis
    results = demo.run_complete_analysis(
        save_results=True, 
        create_visualizations=True
    )
    
    # Demonstrate data management
    demo.demonstrate_data_management()
    
    print("\n" + "=" * 60)
    print("🎯 DEMO HIGHLIGHTS")
    print("=" * 60)
    print("✅ Circle method: Major/minor arc cognitive decomposition")
    print("✅ Sieve theory: Pattern filtering and twin detection")
    print("✅ Laurent expansion: Rich local structure analysis")
    print("✅ Visualization: Comprehensive matplotlib plots")
    print("✅ Data storage: JSON-based persistent storage")
    print("✅ Data analysis: Trend detection and anomaly identification")
    print("✅ Export capabilities: CSV export for external analysis")
    print("\nThis framework demonstrates how analytic number theory")
    print("can enhance cognitive processing with rigorous mathematical")
    print("foundations, comprehensive visualization, and robust data management.")

if __name__ == "__main__":
    main()
