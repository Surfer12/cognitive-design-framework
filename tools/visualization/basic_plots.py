"""
Basic Cognitive Visualization Tools
Simple matplotlib plots for circle method and sieve analysis
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple

def plot_circle_method_simple(data: List[float], 
                             major_arc_indices: List[int],
                             minor_arc_indices: List[int]) -> None:
    """Simple plot showing major vs minor arc classification"""
    
    plt.figure(figsize=(10, 6))
    
    # Plot major arc points
    major_values = [data[i] for i in major_arc_indices]
    plt.scatter(major_arc_indices, major_values, 
               c='blue', label='Major Arc (Rational)', alpha=0.7)
    
    # Plot minor arc points  
    minor_values = [data[i] for i in minor_arc_indices]
    plt.scatter(minor_arc_indices, minor_values,
               c='red', label='Minor Arc (Subtle)', alpha=0.7)
    
    plt.title('Circle Method: Cognitive Arc Classification')
    plt.xlabel('Data Point Index')
    plt.ylabel('Cognitive Value')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

def plot_laurent_expansion(s_values: List[float], 
                          zeta_values: List[float]) -> None:
    """Simple plot of cognitive zeta function"""
    
    plt.figure(figsize=(8, 6))
    
    plt.plot(s_values, zeta_values, 'o-', linewidth=2, markersize=6)
    plt.axvline(x=1.0, color='red', linestyle='--', alpha=0.7, 
               label='Critical point s=1')
    
    plt.title('Cognitive Zeta Function ζ_cog(s)')
    plt.xlabel('s parameter')
    plt.ylabel('ζ_cog(s)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
