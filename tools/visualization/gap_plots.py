"""
Gap Analysis Visualization Tools
Matplotlib plots for cognitive gap detection and analysis
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple

def plot_cognitive_gaps(sequence: List[float], 
                       gaps: List[Tuple[float, float]]) -> None:
    """Plot cognitive sequence with detected gaps highlighted"""
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # Plot 1: Sequence with gaps highlighted
    ax1.plot(sequence, 'o-', color='gray', alpha=0.6, markersize=4,
            label=f'Cognitive Sequence ({len(sequence)} points)')
    
    # Highlight gaps
    if gaps:
        for i, (gap_start, gap_end) in enumerate(gaps):
            # Find indices closest to gap boundaries
            start_idx = min(range(len(sequence)), 
                          key=lambda x: abs(sequence[x] - gap_start))
            end_idx = min(range(len(sequence)), 
                        key=lambda x: abs(sequence[x] - gap_end))
            
            if start_idx < end_idx:
                ax1.axvspan(start_idx, end_idx, alpha=0.3, 
                           color='red', 
                           label='Cognitive Gap' if i == 0 else "")
    
    ax1.set_title(f'Cognitive Sequence with Detected Gaps ({len(gaps)} gaps)')
    ax1.set_xlabel('Sequence Index')
    ax1.set_ylabel('Cognitive Value')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Gap size distribution
    if gaps:
        gap_sizes = [end - start for start, end in gaps]
        ax2.hist(gap_sizes, bins=min(15, len(gaps)), 
                color='red', alpha=0.7, edgecolor='black')
        ax2.set_title('Distribution of Cognitive Gap Sizes')
        ax2.set_xlabel('Gap Size')
        ax2.set_ylabel('Frequency')
        ax2.grid(True, alpha=0.3)
        
        # Add mean line
        if gap_sizes:
            mean_gap = np.mean(gap_sizes)
            ax2.axvline(mean_gap, color='darkred', linestyle='--', 
                       linewidth=2, label=f'Mean: {mean_gap:.3f}')
            ax2.legend()
    else:
        ax2.text(0.5, 0.5, 'No gaps detected', 
                transform=ax2.transAxes, ha='center', va='center',
                fontsize=16, color='gray')
        ax2.set_title('No Cognitive Gaps Found')
    
    plt.tight_layout()
    plt.show()

def plot_gap_statistics(gaps: List[Tuple[float, float]]) -> None:
    """Plot detailed gap statistics"""
    
    if not gaps:
        print("No gaps to analyze")
        return
    
    gap_sizes = [end - start for start, end in gaps]
    gap_positions = [(start + end) / 2 for start, end in gaps]
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    
    # Gap sizes over position
    ax1.scatter(gap_positions, gap_sizes, alpha=0.7, color='red')
    ax1.set_title('Gap Size vs Position')
    ax1.set_xlabel('Gap Center Position')
    ax1.set_ylabel('Gap Size')
    ax1.grid(True, alpha=0.3)
    
    # Gap size histogram with statistics
    ax2.hist(gap_sizes, bins=min(10, len(gaps)), 
            alpha=0.7, color='red', edgecolor='black')
    ax2.axvline(np.mean(gap_sizes), color='darkred', linestyle='--', 
               label=f'Mean: {np.mean(gap_sizes):.3f}')
    ax2.axvline(np.median(gap_sizes), color='blue', linestyle='--', 
               label=f'Median: {np.median(gap_sizes):.3f}')
    ax2.set_title('Gap Size Distribution')
    ax2.set_xlabel('Gap Size')
    ax2.set_ylabel('Frequency')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Cumulative gap sizes
    sorted_gaps = sorted(gap_sizes)
    cumulative = np.cumsum(sorted_gaps)
    ax3.plot(range(len(sorted_gaps)), cumulative, 'o-', color='red')
    ax3.set_title('Cumulative Gap Sizes')
    ax3.set_xlabel('Gap Index (sorted)')
    ax3.set_ylabel('Cumulative Gap Size')
    ax3.grid(True, alpha=0.3)
    
    # Gap statistics summary
    stats_text = f"""Gap Statistics:
Count: {len(gaps)}
Mean Size: {np.mean(gap_sizes):.4f}
Std Dev: {np.std(gap_sizes):.4f}
Min Size: {min(gap_sizes):.4f}
Max Size: {max(gap_sizes):.4f}
Total Gap: {sum(gap_sizes):.4f}"""
    
    ax4.text(0.1, 0.9, stats_text, transform=ax4.transAxes, 
            fontsize=10, verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray"))
    ax4.set_title('Gap Statistics Summary')
    ax4.axis('off')
    
    plt.tight_layout()
    plt.show()

def plot_gap_density_analysis(sequence: List[float], 
                             gaps: List[Tuple[float, float]],
                             window_size: int = 10) -> None:
    """Analyze gap density across the cognitive sequence"""
    
    if not gaps or len(sequence) < window_size:
        print("Insufficient data for density analysis")
        return
    
    # Compute gap density in sliding windows
    densities = []
    positions = []
    
    for i in range(len(sequence) - window_size + 1):
        window_start = sequence[i]
        window_end = sequence[i + window_size - 1]
        
        # Count gaps that overlap with this window
        gap_count = 0
        for gap_start, gap_end in gaps:
            if (gap_start <= window_end and gap_end >= window_start):
                gap_count += 1
        
        density = gap_count / window_size
        densities.append(density)
        positions.append(i + window_size // 2)
    
    plt.figure(figsize=(12, 6))
    
    # Plot density
    plt.plot(positions, densities, 'o-', color='red', alpha=0.7)
    plt.fill_between(positions, densities, alpha=0.3, color='red')
    
    # Add mean density line
    mean_density = np.mean(densities)
    plt.axhline(mean_density, color='darkred', linestyle='--', 
               label=f'Mean Density: {mean_density:.3f}')
    
    plt.title(f'Cognitive Gap Density Analysis (Window Size: {window_size})')
    plt.xlabel('Sequence Position')
    plt.ylabel('Gap Density')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

def plot_gap_pattern_analysis(gaps: List[Tuple[float, float]]) -> None:
    """Analyze patterns in gap spacing and clustering"""
    
    if len(gaps) < 2:
        print("Need at least 2 gaps for pattern analysis")
        return
    
    # Compute gap-to-gap distances
    gap_centers = [(start + end) / 2 for start, end in gaps]
    gap_distances = [gap_centers[i+1] - gap_centers[i] 
                    for i in range(len(gap_centers) - 1)]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Gap spacing analysis
    ax1.plot(range(len(gap_distances)), gap_distances, 'o-', 
            color='red', alpha=0.7)
    ax1.set_title('Gap-to-Gap Distances')
    ax1.set_xlabel('Gap Pair Index')
    ax1.set_ylabel('Distance Between Gap Centers')
    ax1.grid(True, alpha=0.3)
    
    # Add mean distance line
    if gap_distances:
        mean_distance = np.mean(gap_distances)
        ax1.axhline(mean_distance, color='darkred', linestyle='--', 
                   label=f'Mean: {mean_distance:.3f}')
        ax1.legend()
    
    # Gap clustering analysis
    if gap_distances:
        ax2.hist(gap_distances, bins=min(8, len(gap_distances)), 
                alpha=0.7, color='red', edgecolor='black')
        ax2.set_title('Distribution of Gap Spacings')
        ax2.set_xlabel('Distance Between Gaps')
        ax2.set_ylabel('Frequency')
        ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
