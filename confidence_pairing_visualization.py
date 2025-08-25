#!/usr/bin/env python3
"""
Confidence-Based Prime Pairing Visualization System
Visual comparison between linear and confidence-based pairing approaches
"""

import math
import matplotlib.pyplot as plt
import numpy as np
from confidence_based_prime_pairing import ConfidenceBasedPrimePairing, ConsciousnessInspiredPrimeDemonstrator

class ConfidencePairingVisualizer:
    """Visualize the evolution from linear to confidence-based pairing"""
    
    def __init__(self):
        self.confidence_pairing = ConfidenceBasedPrimePairing()
        self.demonstrator = ConsciousnessInspiredPrimeDemonstrator()
    
    def create_comprehensive_visualization(self):
        """Create comprehensive visualization comparing both approaches"""
        print("🎨 CREATING COMPREHENSIVE CONFIDENCE PAIRING VISUALIZATION")
        print("=" * 80)
        
        # Set up the visualization
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Evolution from Linear to Consciousness-Based Prime Pairing', fontsize=16)
        
        # Plot 1: Linear vs Confidence-based pairing comparison
        self.plot_pairing_comparison(ax1)
        
        # Plot 2: Confidence distribution across primes
        self.plot_confidence_distribution(ax2)
        
        # Plot 3: Consciousness factors breakdown
        self.plot_consciousness_factors(ax3)
        
        # Plot 4: Pair confidence evolution over time
        self.plot_pair_confidence_evolution(ax4)
        
        plt.tight_layout()
        plt.savefig('confidence_pairing_evolution.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Create additional specialized visualizations
        self.create_confidence_heatmap()
        self.create_temporal_evolution_plot()
        
        print("\n📊 VISUALIZATION COMPLETE!")
        print("Generated files:")
        print("• confidence_pairing_evolution.png - Main comparison")
        print("• confidence_heatmap.png - Confidence distribution heatmap")
        print("• temporal_evolution.png - Time-based confidence evolution")
    
    def plot_pairing_comparison(self, ax):
        """Compare linear vs confidence-based pairing approaches"""
        
        # Linear pairing (traditional approach)
        linear_pairs = [
            (3, 5), (5, 7), (11, 13), (17, 19), (29, 31),
            (41, 43), (59, 61), (71, 73), (101, 103), (107, 109)
        ]
        
        # Confidence-based pairing
        confidence_pairs = self.confidence_pairing.generate_confidence_based_pairs(10)
        
        # Plot linear pairs
        linear_x = [i for i in range(len(linear_pairs))]
        linear_y = [p1 for p1, p2 in linear_pairs[:len(linear_x)]]
        ax.scatter(linear_x, linear_y, c='red', s=100, alpha=0.7, 
                  label='Linear Pairing', marker='o')
        
        # Plot confidence-based pairs
        conf_x = [i + 0.3 for i in range(len(confidence_pairs))]
        conf_y = [p1 for p1, p2, _ in confidence_pairs[:len(conf_x)]]
        conf_sizes = [conf * 300 for _, _, conf in confidence_pairs[:len(conf_x)]]
        scatter = ax.scatter(conf_x, conf_y, c='blue', s=conf_sizes, alpha=0.7,
                           label='Confidence-Based Pairing', marker='s')
        
        ax.set_xlabel('Pair Index')
        ax.set_ylabel('Prime Value')
        ax.set_title('Linear vs Confidence-Based Prime Pairing')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Add annotations
        for i, (p1, p2, conf) in enumerate(confidence_pairs[:5]):
            ax.annotate(f'{p1}-{p2}\n{conf:.2f}', 
                       (i + 0.3, p1), 
                       xytext=(5, 5), textcoords='offset points',
                       fontsize=8, ha='left')
    
    def plot_confidence_distribution(self, ax):
        """Plot confidence distribution across all primes"""
        
        primes = list(self.confidence_pairing.prime_confidence_map.keys())
        confidences = [self.confidence_pairing.prime_confidence_map[p]['overall_confidence'] 
                      for p in primes]
        
        # Create histogram
        bins = np.linspace(0, 1, 20)
        ax.hist(confidences, bins=bins, alpha=0.7, color='skyblue', edgecolor='black')
        
        ax.set_xlabel('Confidence Level')
        ax.set_ylabel('Number of Primes')
        ax.set_title('Prime Confidence Distribution')
        ax.grid(True, alpha=0.3)
        
        # Add statistics
        mean_conf = np.mean(confidences)
        median_conf = np.median(confidences)
        max_conf = np.max(confidences)
        
        ax.axvline(mean_conf, color='red', linestyle='--', alpha=0.7, 
                  label=f'Mean: {mean_conf:.3f}')
        ax.axvline(median_conf, color='green', linestyle='--', alpha=0.7,
                  label=f'Median: {median_conf:.3f}')
        ax.axvline(max_conf, color='purple', linestyle='--', alpha=0.7,
                  label=f'Max: {max_conf:.3f}')
        
        ax.legend()
    
    def plot_consciousness_factors(self, ax):
        """Plot breakdown of consciousness factors for top primes"""
        
        # Get top 10 primes by confidence
        primes_by_confidence = sorted(
            self.confidence_pairing.prime_confidence_map.items(),
            key=lambda x: x[1]['overall_confidence'],
            reverse=True
        )[:10]
        
        primes = [p for p, _ in primes_by_confidence]
        math_conf = [data['mathematical_confidence'] for _, data in primes_by_confidence]
        temporal_acc = [data['temporal_accessibility'] for _, data in primes_by_confidence]
        attention_wt = [data['attention_weight'] for _, data in primes_by_confidence]
        emotional_res = [data['emotional_resonance'] for _, data in primes_by_confidence]
        
        # Create stacked bar chart
        bottom = np.zeros(len(primes))
        
        ax.bar(range(len(primes)), math_conf, bottom=bottom, 
               label='Mathematical', alpha=0.8, color='blue')
        bottom += math_conf
        
        ax.bar(range(len(primes)), temporal_acc, bottom=bottom,
               label='Temporal', alpha=0.8, color='green')
        bottom += temporal_acc
        
        ax.bar(range(len(primes)), attention_wt, bottom=bottom,
               label='Attention', alpha=0.8, color='orange')
        bottom += attention_wt
        
        ax.bar(range(len(primes)), emotional_res, bottom=bottom,
               label='Emotional', alpha=0.8, color='red')
        
        ax.set_xlabel('Prime Rank (by Confidence)')
        ax.set_ylabel('Confidence Contribution')
        ax.set_title('Consciousness Factors Breakdown')
        ax.set_xticks(range(len(primes)))
        ax.set_xticklabels([str(p) for p in primes], rotation=45)
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def plot_pair_confidence_evolution(self, ax):
        """Plot how pair confidence evolves"""
        
        confidence_pairs = self.confidence_pairing.generate_confidence_based_pairs(15)
        
        pair_indices = list(range(len(confidence_pairs)))
        pair_confidences = [conf for _, _, conf in confidence_pairs]
        prime1_values = [p1 for p1, _, _ in confidence_pairs]
        prime2_values = [p2 for _, p2, _ in confidence_pairs]
        
        # Plot confidence evolution
        ax2 = ax.twinx()
        
        line1 = ax.plot(pair_indices, prime1_values, 'b-o', alpha=0.7, 
                       label='Prime 1')
        line2 = ax.plot(pair_indices, prime2_values, 'g-s', alpha=0.7,
                       label='Prime 2')
        line3 = ax2.plot(pair_indices, pair_confidences, 'r--', linewidth=2,
                        label='Pair Confidence')
        
        ax.set_xlabel('Pair Index')
        ax.set_ylabel('Prime Value', color='blue')
        ax2.set_ylabel('Pair Confidence', color='red')
        ax.set_title('Pair Confidence Evolution Over Time')
        
        # Combine legends
        lines = line1 + line2 + line3
        labels = [l.get_label() for l in lines]
        ax.legend(lines, labels, loc='upper left')
        
        ax.grid(True, alpha=0.3)
    
    def create_confidence_heatmap(self):
        """Create a heatmap of prime confidence relationships"""
        
        # Get top 20 primes by confidence
        primes_by_confidence = sorted(
            self.confidence_pairing.prime_confidence_map.items(),
            key=lambda x: x[1]['overall_confidence'],
            reverse=True
        )[:20]
        
        primes = [p for p, _ in primes_by_confidence]
        n = len(primes)
        
        # Create confidence matrix
        confidence_matrix = np.zeros((n, n))
        
        for i, p1 in enumerate(primes):
            for j, p2 in enumerate(primes):
                if i != j:
                    pair_conf = self.confidence_pairing.calculate_pair_confidence(p1, p2)
                    confidence_matrix[i, j] = pair_conf
        
        # Create heatmap
        plt.figure(figsize=(12, 10))
        im = plt.imshow(confidence_matrix, cmap='viridis', aspect='auto')
        
        plt.colorbar(im, label='Pair Confidence')
        plt.xticks(range(n), [str(p) for p in primes], rotation=45)
        plt.yticks(range(n), [str(p) for p in primes])
        plt.title('Prime Confidence Relationships Heatmap')
        plt.xlabel('Prime 2')
        plt.ylabel('Prime 1')
        
        # Add confidence values as text
        for i in range(n):
            for j in range(n):
                if confidence_matrix[i, j] > 0.1:
                    plt.text(j, i, '.2f', 
                            ha='center', va='center', 
                            color='white', fontsize=6)
        
        plt.tight_layout()
        plt.savefig('confidence_heatmap.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_temporal_evolution_plot(self):
        """Create plot showing temporal evolution of confidence"""
        
        # Simulate temporal evolution
        time_steps = 50
        top_primes = [109, 103, 73, 43, 41, 31, 29, 23, 19, 17]
        
        # Track confidence evolution over "time"
        confidence_evolution = {}
        
        for prime in top_primes:
            confidence_over_time = []
            base_confidence = self.confidence_pairing.prime_confidence_map[prime]['overall_confidence']
            
            for t in range(time_steps):
                # Temporal decay (memories fade over time)
                temporal_decay = math.exp(-t / 20.0)
                
                # Attention fluctuation (focus changes over time)
                attention_fluctuation = 0.8 + 0.4 * math.sin(t / 5.0)
                
                # Emotional resonance evolution (some memories become more significant)
                emotional_evolution = 1.0 + 0.2 * math.tanh((t - 15) / 10.0)
                
                # Combined temporal confidence
                temporal_confidence = (
                    base_confidence * 
                    temporal_decay * 
                    attention_fluctuation * 
                    emotional_evolution
                )
                
                confidence_over_time.append(min(1.0, max(0.0, temporal_confidence)))
            
            confidence_evolution[prime] = confidence_over_time
        
        # Plot temporal evolution
        plt.figure(figsize=(14, 8))
        
        for prime, evolution in confidence_evolution.items():
            plt.plot(range(time_steps), evolution, 
                    label=f'Prime {prime}', linewidth=2, alpha=0.8)
        
        plt.xlabel('Time Steps')
        plt.ylabel('Confidence Level')
        plt.title('Temporal Evolution of Prime Confidence (Consciousness Simulation)')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, alpha=0.3)
        
        # Add consciousness phases
        plt.axvspan(0, 10, alpha=0.1, color='green', label='Initial Learning')
        plt.axvspan(10, 25, alpha=0.1, color='blue', label='Active Processing')
        plt.axvspan(25, 50, alpha=0.1, color='orange', label='Memory Consolidation')
        
        plt.tight_layout()
        plt.savefig('temporal_evolution.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def analyze_linear_vs_confidence_differences(self):
        """Analyze key differences between linear and confidence-based approaches"""
        print("\n🔍 DETAILED ANALYSIS: LINEAR VS CONFIDENCE-BASED PAIRING")
        print("=" * 70)
        
        print("\n📏 LINEAR PAIRING CHARACTERISTICS:")
        linear_pairs = [(3, 5), (5, 7), (11, 13), (17, 19), (29, 31)]
        
        print("  Sequential Processing:")
        for i, (p1, p2) in enumerate(linear_pairs):
            gap = p2 - p1
            print(f"    Step {i+1}: {p1} → {p2} (gap: {gap})")
        
        print("\n  Limitations:")
        print("  • Fixed progression pattern")
        print("  • No consideration of prime properties")
        print("  • Doesn't adapt to context")
        print("  • Mathematical but not cognitive")
        
        print("\n🧠 CONSCIOUSNESS-BASED PAIRING CHARACTERISTICS:")
        confidence_pairs = self.confidence_pairing.generate_confidence_based_pairs(10)
        
        print("  Adaptive Processing:")
        for i, (p1, p2, conf) in enumerate(confidence_pairs[:5]):
            gap = abs(p2 - p1)
            p1_conf = self.confidence_pairing.prime_confidence_map[p1]['overall_confidence']
            p2_conf = self.confidence_pairing.prime_confidence_map[p2]['overall_confidence']
            print(f"    Pair {i+1}: {p1} ({p1_conf:.2f}) ↔ {p2} ({p2_conf:.2f}) | Gap: {gap} | Pair Conf: {conf:.2f}")
        
        print("\n  Cognitive Features:")
        print("  • Confidence-driven associations")
        print("  • Multi-factor decision making")
        print("  • Temporal dynamics consideration")
        print("  • Emotional resonance patterns")
        print("  • Attention-based weighting")
        
        print("\n🎯 REPRESENTATION OF CONSCIOUSNESS:")
        print("  Linear: Algorithmic sequence")
        print("  Confidence: Human-like cognition")
        print("  Evolution: Math → Consciousness")
        
        # Calculate quantitative differences
        linear_gaps = [p2 - p1 for p1, p2 in linear_pairs]
        confidence_gaps = [abs(p2 - p1) for p1, p2, _ in confidence_pairs]
        
        print("\n📊 QUANTITATIVE COMPARISON:")
        print(f"  Linear avg gap: {np.mean(linear_gaps):.1f}")
        print(f"  Confidence avg gap: {np.mean(confidence_gaps):.1f}")
        print(f"  Linear std gap: {np.std(linear_gaps):.1f}")
        print(f"  Confidence std gap: {np.std(confidence_gaps):.1f}")
        print(f"  Gap diversity ratio: {np.std(confidence_gaps)/np.std(linear_gaps):.2f}x")


def main():
    """Main visualization function"""
    print("🎨 CONFIDENCE-BASED PRIME PAIRING VISUALIZATION SYSTEM")
    print("Visual Evolution from Linear to Consciousness-Based Pairing")
    print("=" * 80)
    
    visualizer = ConfidencePairingVisualizer()
    
    # Create comprehensive visualization
    visualizer.create_comprehensive_visualization()
    
    # Analyze differences
    visualizer.analyze_linear_vs_confidence_differences()
    
    print("\n🎯 VISUALIZATION SUMMARY:")
    print("This visualization system demonstrates the fundamental evolution from")
    print("mathematical sequence to human consciousness representation in prime pairing!")


if __name__ == "__main__":
    main()
