"""
Cognitive Analysis Visualization Tools
Uses matplotlib to visualize circle method, sieve theory, and Laurent expansion results
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle
import numpy as np
import json
from typing import List, Dict, Tuple, Any
from pathlib import Path

class CognitiveVisualizer:
    """Visualization tools for cognitive analysis results"""
    
    def __init__(self, style: str = 'seaborn-v0_8', figsize: Tuple[int, int] = (12, 8)):
        """Initialize visualizer with style preferences"""
        plt.style.use(style)
        self.figsize = figsize
        self.colors = {
            'major_arc': '#2E86AB',
            'minor_arc': '#A23B72', 
            'cognitive_prime': '#F18F01',
            'filtered': '#C73E1D',
            'twin_pair': '#7209B7',
            'gap': '#FF6B6B',
            'zeta': '#4ECDC4'
        }
    
    def plot_circle_method_decomposition(self, data: List[float], 
                                       arc_classifications: List[bool],
                                       contributions: List[float],
                                       save_path: str = None) -> None:
        """
        Visualize circle method decomposition of cognitive data
        
        Args:
            data: Original cognitive input values
            arc_classifications: True for major arc, False for minor arc
            contributions: Contribution values from each arc
            save_path: Optional path to save the plot
        """
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=self.figsize)
        
        # Plot 1: Original data with arc classification
        major_indices = [i for i, is_major in enumerate(arc_classifications) if is_major]
        minor_indices = [i for i, is_major in enumerate(arc_classifications) if not is_major]
        
        ax1.scatter([i for i in major_indices], [data[i] for i in major_indices], 
                   c=self.colors['major_arc'], label='Major Arc (Rational)', alpha=0.7, s=50)
        ax1.scatter([i for i in minor_indices], [data[i] for i in minor_indices],
                   c=self.colors['minor_arc'], label='Minor Arc (Subtle)', alpha=0.7, s=50)
        
        ax1.set_title('Circle Method: Major vs Minor Arc Classification')
        ax1.set_xlabel('Data Point Index')
        ax1.set_ylabel('Cognitive Value')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Contribution values
        ax2.bar(range(len(contributions)), contributions, 
               color=[self.colors['major_arc'] if is_major else self.colors['minor_arc'] 
                     for is_major in arc_classifications], alpha=0.7)
        ax2.set_title('Arc Contributions to Cognitive Processing')
        ax2.set_xlabel('Data Point Index')
        ax2.set_ylabel('Contribution Value')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Cumulative analysis
        major_cumsum = np.cumsum([contrib if is_major else 0 
                                 for contrib, is_major in zip(contributions, arc_classifications)])
        minor_cumsum = np.cumsum([contrib if not is_major else 0 
                                 for contrib, is_major in zip(contributions, arc_classifications)])
        
        ax3.plot(major_cumsum, color=self.colors['major_arc'], 
                label='Cumulative Major Arc', linewidth=2)
        ax3.plot(minor_cumsum, color=self.colors['minor_arc'], 
                label='Cumulative Minor Arc', linewidth=2)
        ax3.fill_between(range(len(major_cumsum)), major_cumsum, alpha=0.3, 
                        color=self.colors['major_arc'])
        ax3.fill_between(range(len(minor_cumsum)), minor_cumsum, alpha=0.3, 
                        color=self.colors['minor_arc'])
        
        ax3.set_title('Cumulative Cognitive Processing Contributions')
        ax3.set_xlabel('Data Point Index')
        ax3.set_ylabel('Cumulative Contribution')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Circle method plot saved to: {save_path}")
        
        plt.show()
    
    def plot_sieve_analysis(self, original_data: List[float], 
                           filtered_data: List[float],
                           twin_pairs: List[Tuple[float, float]],
                           prime_patterns: List[int],
                           save_path: str = None) -> None:
        """
        Visualize sieve theory filtering results
        
        Args:
            original_data: Original cognitive input
            filtered_data: Data after Selberg sieve filtering
            twin_pairs: Cognitive twin pairs found by Brun sieve
            prime_patterns: Prime cognitive patterns used in sieve
            save_path: Optional path to save the plot
        """
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=self.figsize)
        
        # Plot 1: Original vs Filtered Data
        ax1.hist(original_data, bins=30, alpha=0.7, color='gray', 
                label=f'Original ({len(original_data)} points)', density=True)
        ax1.hist(filtered_data, bins=20, alpha=0.8, color=self.colors['filtered'], 
                label=f'Filtered ({len(filtered_data)} points)', density=True)
        ax1.set_title('Selberg Sieve Filtering Effect')
        ax1.set_xlabel('Cognitive Value')
        ax1.set_ylabel('Density')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Twin Pairs Visualization
        if twin_pairs:
            twin_x = [pair[0] for pair in twin_pairs]
            twin_y = [pair[1] for pair in twin_pairs]
            ax2.scatter(twin_x, twin_y, c=self.colors['twin_pair'], 
                       s=60, alpha=0.7, label='Twin Pairs')
            
            # Draw lines connecting twin pairs
            for pair in twin_pairs:
                ax2.plot([pair[0], pair[1]], [pair[0], pair[1]], 
                        color=self.colors['twin_pair'], alpha=0.3, linewidth=1)
            
            # Add diagonal line for reference
            min_val, max_val = min(min(twin_x), min(twin_y)), max(max(twin_x), max(twin_y))
            ax2.plot([min_val, max_val], [min_val, max_val], 
                    'k--', alpha=0.5, label='y=x reference')
        
        ax2.set_title(f'Brun Sieve: Cognitive Twin Pairs ({len(twin_pairs)} found)')
        ax2.set_xlabel('First Twin Value')
        ax2.set_ylabel('Second Twin Value')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Prime Pattern Distribution
        ax3.bar(range(len(prime_patterns[:20])), prime_patterns[:20], 
               color=self.colors['cognitive_prime'], alpha=0.7)
        ax3.set_title('Cognitive Prime Patterns (First 20)')
        ax3.set_xlabel('Pattern Index')
        ax3.set_ylabel('Pattern Value')
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Sieve Effectiveness
        retention_rate = len(filtered_data) / len(original_data) if original_data else 0
        twin_rate = len(twin_pairs) / len(filtered_data) if filtered_data else 0
        
        categories = ['Retention\nRate', 'Twin Pair\nRate']
        values = [retention_rate, twin_rate]
        colors = [self.colors['filtered'], self.colors['twin_pair']]
        
        bars = ax4.bar(categories, values, color=colors, alpha=0.7)
        ax4.set_title('Sieve Analysis Metrics')
        ax4.set_ylabel('Rate')
        ax4.set_ylim(0, 1)
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{value:.3f}', ha='center', va='bottom')
        
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Sieve analysis plot saved to: {save_path}")
        
        plt.show()
    
    def plot_laurent_expansion(self, s_values: List[float], 
                              zeta_values: List[float],
                              local_richness: List[float],
                              save_path: str = None) -> None:
        """
        Visualize Laurent expansion analysis around cognitive critical point
        
        Args:
            s_values: s-parameter values
            zeta_values: Cognitive zeta function values
            local_richness: Local structure richness measures
            save_path: Optional path to save the plot
        """
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=self.figsize)
        
        # Plot 1: Cognitive Zeta Function
        ax1.plot(s_values, zeta_values, 'o-', color=self.colors['zeta'], 
                linewidth=2, markersize=6, label='ζ_cognitive(s)')
        ax1.axvline(x=1.0, color='red', linestyle='--', alpha=0.7, 
                   label='Critical point s=1')
        ax1.set_title('Cognitive Zeta Function ζ_cog(s)')
        ax1.set_xlabel('s parameter')
        ax1.set_ylabel('ζ_cog(s)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Highlight the pole region
        pole_region = patches.Rectangle((0.95, min(zeta_values)), 0.1, 
                                      max(zeta_values) - min(zeta_values),
                                      linewidth=1, edgecolor='red', 
                                      facecolor='red', alpha=0.1)
        ax1.add_patch(pole_region)
        
        # Plot 2: Local Structure Richness
        ax2.plot(s_values, local_richness, 's-', color=self.colors['major_arc'], 
                linewidth=2, markersize=8, label='Local Structure Richness')
        ax2.axvline(x=1.0, color='red', linestyle='--', alpha=0.7)
        ax2.axhline(y=0.5, color='gray', linestyle=':', alpha=0.5, 
                   label='50% richness threshold')
        ax2.set_title('Laurent Expansion: Regular vs Singular Contribution')
        ax2.set_xlabel('s parameter')
        ax2.set_ylabel('Richness (Regular Part Ratio)')
        ax2.set_ylim(0, 1)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Combined Analysis
        # Normalize both series for comparison
        zeta_norm = np.array(zeta_values) / max(abs(z) for z in zeta_values)
        
        ax3.plot(s_values, zeta_norm, 'o-', color=self.colors['zeta'], 
                linewidth=2, label='ζ_cog(s) (normalized)', alpha=0.7)
        ax3.plot(s_values, local_richness, 's-', color=self.colors['major_arc'], 
                linewidth=2, label='Local Richness', alpha=0.7)
        ax3.axvline(x=1.0, color='red', linestyle='--', alpha=0.7, 
                   label='Critical point')
        
        ax3.set_title('Laurent Analysis: Function Behavior vs Local Structure')
        ax3.set_xlabel('s parameter')
        ax3.set_ylabel('Normalized Value')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Laurent expansion plot saved to: {save_path}")
        
        plt.show()
    
    def plot_cognitive_gaps(self, sequence: List[float], 
                           gaps: List[Tuple[float, float]],
                           save_path: str = None) -> None:
        """
        Visualize cognitive gaps in processing
        
        Args:
            sequence: Original cognitive sequence
            gaps: Detected gaps as (start, end) tuples
            save_path: Optional path to save the plot
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=self.figsize)
        
        # Plot 1: Sequence with gaps highlighted
        ax1.plot(sequence, 'o-', color='gray', alpha=0.6, 
                label=f'Cognitive Sequence ({len(sequence)} points)')
        
        # Highlight gaps
        for i, (gap_start, gap_end) in enumerate(gaps):
            # Find indices closest to gap boundaries
            start_idx = min(range(len(sequence)), 
                          key=lambda x: abs(sequence[x] - gap_start))
            end_idx = min(range(len(sequence)), 
                        key=lambda x: abs(sequence[x] - gap_end))
            
            if start_idx < end_idx:
                ax1.axvspan(start_idx, end_idx, alpha=0.3, 
                           color=self.colors['gap'], 
                           label='Cognitive Gap' if i == 0 else "")
        
        ax1.set_title(f'Cognitive Sequence with Detected Gaps ({len(gaps)} gaps)')
        ax1.set_xlabel('Sequence Index')
        ax1.set_ylabel('Cognitive Value')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Gap size distribution
        if gaps:
            gap_sizes = [end - start for start, end in gaps]
            ax2.hist(gap_sizes, bins=min(20, len(gaps)), 
                    color=self.colors['gap'], alpha=0.7, edgecolor='black')
            ax2.set_title('Distribution of Cognitive Gap Sizes')
            ax2.set_xlabel('Gap Size')
            ax2.set_ylabel('Frequency')
            ax2.grid(True, alpha=0.3)
            
            # Add statistics
            mean_gap = np.mean(gap_sizes)
            ax2.axvline(mean_gap, color='red', linestyle='--', 
                       label=f'Mean: {mean_gap:.3f}')
            ax2.legend()
        else:
            ax2.text(0.5, 0.5, 'No gaps detected', 
                    transform=ax2.transAxes, ha='center', va='center',
                    fontsize=16, color='gray')
            ax2.set_title('No Cognitive Gaps Found')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Cognitive gaps plot saved to: {save_path}")
        
        plt.show()
    
    def plot_integrated_dashboard(self, results: Dict[str, Any], 
                                 save_path: str = None) -> None:
        """
        Create comprehensive dashboard of all cognitive analysis results
        
        Args:
            results: Dictionary containing all analysis results
            save_path: Optional path to save the plot
        """
        fig = plt.figure(figsize=(16, 12))
        
        # Create grid layout
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # Plot 1: Major vs Minor Arc Ratio (top-left)
        ax1 = fig.add_subplot(gs[0, 0])
        ratio = results.get('major_minor_ratio', 1.0)
        wedges, texts, autotexts = ax1.pie([ratio, 1], 
                                          labels=['Major Arc', 'Minor Arc'],
                                          colors=[self.colors['major_arc'], 
                                                 self.colors['minor_arc']],
                                          autopct='%1.1f%%', startangle=90)
        ax1.set_title('Cognitive Processing\nArc Distribution')
        
        # Plot 2: Zeta Function Value (top-center)
        ax2 = fig.add_subplot(gs[0, 1])
        zeta_val = results.get('cognitive_zeta', 0)
        ax2.bar(['ζ_cog(s)'], [zeta_val], color=self.colors['zeta'], alpha=0.7)
        ax2.set_title('Cognitive Zeta\nFunction Value')
        ax2.set_ylabel('ζ_cog(s)')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Local Structure Richness (top-right)
        ax3 = fig.add_subplot(gs[0, 2])
        richness = results.get('local_structure_richness', 0)
        ax3.bar(['Richness'], [richness], color=self.colors['major_arc'], alpha=0.7)
        ax3.set_title('Local Structure\nRichness')
        ax3.set_ylabel('Richness Ratio')
        ax3.set_ylim(0, 1)
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Arc Averages Comparison (middle-left)
        ax4 = fig.add_subplot(gs[1, 0])
        major_avg = results.get('major_arc_average', 0)
        minor_avg = results.get('minor_arc_average', 0)
        ax4.bar(['Major Arc', 'Minor Arc'], [major_avg, minor_avg],
               color=[self.colors['major_arc'], self.colors['minor_arc']], 
               alpha=0.7)
        ax4.set_title('Average Arc\nContributions')
        ax4.set_ylabel('Average Contribution')
        ax4.grid(True, alpha=0.3)
        
        # Plot 5: Sieve Dimension (middle-center)
        ax5 = fig.add_subplot(gs[1, 1])
        dimension = results.get('sieve_dimension', 0)
        ax5.bar(['Dimension'], [dimension], color=self.colors['filtered'], alpha=0.7)
        ax5.set_title('Sieve-Estimated\nCognitive Dimension')
        ax5.set_ylabel('Dimension')
        ax5.grid(True, alpha=0.3)
        
        # Plot 6: Processing Summary (middle-right)
        ax6 = fig.add_subplot(gs[1, 2])
        metrics = ['Major/Minor\nRatio', 'Zeta\nValue', 'Richness', 'Dimension']
        values = [ratio, abs(zeta_val), richness, dimension]
        # Normalize for radar-like comparison
        max_val = max(values) if max(values) > 0 else 1
        normalized_values = [v/max_val for v in values]
        
        bars = ax6.bar(metrics, normalized_values, 
                      color=[self.colors['major_arc'], self.colors['zeta'], 
                            self.colors['major_arc'], self.colors['filtered']], 
                      alpha=0.7)
        ax6.set_title('Normalized Metrics\nComparison')
        ax6.set_ylabel('Normalized Value')
        ax6.set_ylim(0, 1)
        plt.setp(ax6.get_xticklabels(), rotation=45, ha='right')
        ax6.grid(True, alpha=0.3)
        
        # Plot 7-9: Summary text and statistics (bottom row)
        ax7 = fig.add_subplot(gs[2, :])
        ax7.axis('off')
        
        # Create summary text
        summary_text = f"""
        COGNITIVE ANALYSIS SUMMARY
        
        Circle Method Analysis:
        • Major Arc Average: {major_avg:.4f}
        • Minor Arc Average: {minor_avg:.4f}  
        • Major/Minor Ratio: {ratio:.4f}
        
        Laurent Expansion Analysis:
        • Cognitive Zeta ζ_cog(s): {zeta_val:.4f}
        • Local Structure Richness: {richness:.4f}
        
        Sieve Theory Analysis:
        • Estimated Cognitive Dimension: {dimension:.4f}
        
        Interpretation:
        • Higher major/minor ratio indicates more rational processing
        • Local richness shows contribution beyond singular behavior
        • Cognitive dimension estimates complexity of pattern space
        """
        
        ax7.text(0.05, 0.95, summary_text, transform=ax7.transAxes, 
                fontsize=10, verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.8))
        
        plt.suptitle('🧠 Analytic Number Theory Cognitive Analysis Dashboard', 
                    fontsize=16, fontweight='bold')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Integrated dashboard saved to: {save_path}")
        
        plt.show()
