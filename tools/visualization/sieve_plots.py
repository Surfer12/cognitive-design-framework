"""
Sieve Theory Visualization Tools
Matplotlib plots for sieve analysis results
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple

def plot_sieve_filtering(original_data: List[float], 
                        filtered_data: List[float]) -> None:
    """Plot before/after sieve filtering comparison"""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Original data histogram
    ax1.hist(original_data, bins=20, alpha=0.7, color='gray', 
             label=f'Original ({len(original_data)} points)')
    ax1.set_title('Before Sieve Filtering')
    ax1.set_xlabel('Cognitive Value')
    ax1.set_ylabel('Frequency')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Filtered data histogram
    ax2.hist(filtered_data, bins=15, alpha=0.7, color='blue',
             label=f'Filtered ({len(filtered_data)} points)')
    ax2.set_title('After Selberg Sieve')
    ax2.set_xlabel('Cognitive Value')
    ax2.set_ylabel('Frequency')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def plot_twin_pairs(twin_pairs: List[Tuple[float, float]]) -> None:
    """Plot cognitive twin pairs found by Brun sieve"""
    
    if not twin_pairs:
        print("No twin pairs to plot")
        return
    
    plt.figure(figsize=(8, 6))
    
    # Extract twin values
    twin_x = [pair[0] for pair in twin_pairs]
    twin_y = [pair[1] for pair in twin_pairs]
    
    # Scatter plot of twin pairs
    plt.scatter(twin_x, twin_y, c='purple', s=60, alpha=0.7, 
               label=f'Twin Pairs ({len(twin_pairs)})')
    
    # Draw lines connecting twins
    for pair in twin_pairs:
        plt.plot([pair[0], pair[1]], [pair[0], pair[1]], 
                'purple', alpha=0.3, linewidth=1)
    
    # Add diagonal reference line
    if twin_x and twin_y:
        min_val = min(min(twin_x), min(twin_y))
        max_val = max(max(twin_x), max(twin_y))
        plt.plot([min_val, max_val], [min_val, max_val], 
                'k--', alpha=0.5, label='y=x reference')
    
    plt.title('Brun Sieve: Cognitive Twin Pairs')
    plt.xlabel('First Twin Value')
    plt.ylabel('Second Twin Value')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

def plot_prime_patterns(prime_patterns: List[int], max_show: int = 20) -> None:
    """Plot cognitive prime patterns used in sieve"""
    
    plt.figure(figsize=(10, 6))
    
    # Show first max_show patterns
    patterns_to_show = prime_patterns[:max_show]
    
    plt.bar(range(len(patterns_to_show)), patterns_to_show, 
           color='orange', alpha=0.7)
    plt.title(f'Cognitive Prime Patterns (First {len(patterns_to_show)})')
    plt.xlabel('Pattern Index')
    plt.ylabel('Pattern Value')
    plt.grid(True, alpha=0.3)
    
    # Add value labels on bars
    for i, val in enumerate(patterns_to_show):
        plt.text(i, val + max(patterns_to_show) * 0.01, str(val), 
                ha='center', va='bottom', fontsize=8)
    
    plt.show()

def plot_sieve_effectiveness(original_count: int, 
                           filtered_count: int,
                           twin_count: int) -> None:
    """Plot sieve analysis effectiveness metrics"""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Retention rates
    retention_rate = filtered_count / original_count if original_count > 0 else 0
    twin_rate = twin_count / filtered_count if filtered_count > 0 else 0
    
    categories = ['Data\nRetention', 'Twin Pair\nRate']
    rates = [retention_rate, twin_rate]
    colors = ['blue', 'purple']
    
    bars1 = ax1.bar(categories, rates, color=colors, alpha=0.7)
    ax1.set_title('Sieve Analysis Rates')
    ax1.set_ylabel('Rate (0-1)')
    ax1.set_ylim(0, 1)
    ax1.grid(True, alpha=0.3)
    
    # Add value labels
    for bar, rate in zip(bars1, rates):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                f'{rate:.3f}', ha='center', va='bottom')
    
    # Data counts
    counts = [original_count, filtered_count, twin_count]
    labels = ['Original', 'Filtered', 'Twin Pairs']
    colors2 = ['gray', 'blue', 'purple']
    
    bars2 = ax2.bar(labels, counts, color=colors2, alpha=0.7)
    ax2.set_title('Data Point Counts')
    ax2.set_ylabel('Count')
    ax2.grid(True, alpha=0.3)
    
    # Add value labels
    for bar, count in zip(bars2, counts):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + max(counts) * 0.01,
                str(count), ha='center', va='bottom')
    
    plt.tight_layout()
    plt.show()
