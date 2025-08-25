#!/usr/bin/env python3
"""
Family-Friendly Two Cars Comparison: Wall Agreement vs Traditional AI
Emotional impact through direct side-by-side emergency scenario
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np
import textwrap

def create_two_cars_comparison():
    """Create side-by-side comparison of two cars in emergency scenario"""
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))
    fig.suptitle('🚗 Two Cars, Same Emergency: Wall Agreement vs Traditional AI\nThe Critical Difference in Life-Saving Decisions', 
                 fontsize=18, fontweight='bold', y=0.95)
    
    # Plot 1: Traditional AI Car (Left side)
    ax1.set_title('❌ Car A: Traditional AI (Inconsistent Decisions)', fontsize=14, fontweight='bold', color='red')
    create_traditional_ai_car(ax1)
    
    # Plot 2: Wall Agreement Car (Right side)  
    ax2.set_title('✅ Car B: Ryan\'s Wall Agreement (Perfect Alignment)', fontsize=14, fontweight='bold', color='green')
    create_wall_agreement_car(ax2)
    
    # Plot 3: Emotional Impact Comparison
    ax3.set_title('💝 Emotional Impact: Family Experience', fontsize=14, fontweight='bold')
    create_emotional_impact_comparison(ax3)
    
    # Plot 4: Decision Consistency Over Time
    ax4.set_title('📊 Decision Consistency: 100 Similar Emergencies', fontsize=14, fontweight='bold')
    create_consistency_comparison(ax4)
    
    plt.tight_layout()
    plt.savefig('family_two_cars_comparison.png', dpi=300, bbox_inches='tight', 
                facecolor='lightcyan', edgecolor='none')
    plt.show()
    
    print("🚗 TWO CARS COMPARISON VISUALIZATION CREATED!")
    print("📁 File saved as: family_two_cars_comparison.png")
    print("\n📖 WHAT YOUR FAMILY WILL SEE:")
    print("• Same emergency, two different cars")
    print("• Traditional AI: Inconsistent, unpredictable")
    print("• Ryan's Wall Agreement: Consistent, trustworthy")
    print("• Real emotional impact on family decisions")
    print("• Why consistency matters for safety and trust")

def create_traditional_ai_car(ax):
    """Create visualization of traditional AI car in emergency"""
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    # Road and scenario
    ax.add_patch(patches.Rectangle((0.1, 0.3), 0.8, 0.4, facecolor='lightgray', alpha=0.5))
    ax.text(0.5, 0.65, 'EMERGENCY ROAD SCENARIO', ha='center', fontsize=10, fontweight='bold')
    
    # Child and wall
    ax.add_patch(patches.Circle((0.75, 0.5), 0.03, facecolor='red', alpha=0.9))
    ax.text(0.75, 0.55, 'CHILD', ha='center', fontsize=8, color='red', fontweight='bold')
    
    ax.add_patch(patches.Rectangle((0.82, 0.4), 0.05, 0.2, facecolor='black', alpha=0.8))
    ax.text(0.845, 0.55, 'WALL', ha='center', fontsize=8, color='white', fontweight='bold')
    
    # Traditional AI Car
    ax.add_patch(patches.Rectangle((0.4, 0.45), 0.12, 0.06, facecolor='red', alpha=0.8))
    ax.text(0.46, 0.48, 'TRADITIONAL\nAI CAR', ha='center', fontsize=7, fontweight='bold')
    
    # Conflicting AI systems (shown as arguing)
    ai_systems = [
        ('📊 Data: 70% risk', 0.15, 0.8, 'orange'),
        ('💝 Ethics: Save child', 0.15, 0.7, 'blue'),
        ('⚡ Speed: Swerve now', 0.15, 0.6, 'green'),
        ('🏗️ Risk: Wall damage', 0.15, 0.5, 'purple')
    ]
    
    for system, x, y, color in ai_systems:
        ax.add_patch(FancyBboxPatch((x, y-0.03), 0.25, 0.05, 
                                   boxstyle="round,pad=0.01", facecolor=color, alpha=0.7))
        ax.text(x + 0.125, y, system, ha='center', fontsize=6)
    
    # Conflicting arrows
    ax.arrow(0.46, 0.48, 0.1, 0.05, head_width=0.02, head_length=0.02, 
             fc='red', ec='red', alpha=0.7, linewidth=2)
    ax.text(0.52, 0.52, 'SWERVE', ha='center', fontsize=8, color='red')
    
    ax.arrow(0.46, 0.48, 0.15, 0.0, head_width=0.02, head_length=0.02, 
             fc='blue', ec='blue', alpha=0.7, linewidth=2)
    ax.text(0.57, 0.49, 'CONTINUE', ha='center', fontsize=8, color='blue')
    
    # Inconsistency warning
    ax.add_patch(FancyBboxPatch((0.3, 0.2), 0.4, 0.15, 
                               boxstyle="round,pad=0.02", facecolor='yellow', alpha=0.8))
    ax.text(0.5, 0.3, '⚠️ SYSTEMS DISAGREE!\nDifferent decision each time\nFamily never knows what to expect', 
            ha='center', fontsize=8, wrap=True)
    
    # Emotional impact
    ax.text(0.5, 0.1, '😰 Family Anxiety: "Will it choose right this time?"', 
            ha='center', fontsize=9, color='red', fontweight='bold')

def create_wall_agreement_car(ax):
    """Create visualization of wall agreement car in same emergency"""
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    # Same road and scenario
    ax.add_patch(patches.Rectangle((0.1, 0.3), 0.8, 0.4, facecolor='lightgray', alpha=0.5))
    ax.text(0.5, 0.65, 'SAME EMERGENCY ROAD SCENARIO', ha='center', fontsize=10, fontweight='bold')
    
    # Same child and wall
    ax.add_patch(patches.Circle((0.75, 0.5), 0.03, facecolor='red', alpha=0.9))
    ax.text(0.75, 0.55, 'CHILD', ha='center', fontsize=8, color='red', fontweight='bold')
    
    ax.add_patch(patches.Rectangle((0.82, 0.4), 0.05, 0.2, facecolor='black', alpha=0.8))
    ax.text(0.845, 0.55, 'WALL', ha='center', fontsize=8, color='white', fontweight='bold')
    
    # Wall Agreement Car
    ax.add_patch(patches.Rectangle((0.4, 0.45), 0.12, 0.06, facecolor='green', alpha=0.8))
    ax.text(0.46, 0.48, 'RYAN\'S\nWALL AGREEMENT\nCAR', ha='center', fontsize=6, fontweight='bold')
    
    # Aligned AI systems
    aligned_systems = [
        ('📊 Data: 70% risk (conf: 0.85)', 0.15, 0.8, 'lightblue'),
        ('💝 Ethics: Save child (conf: 0.92)', 0.15, 0.7, 'lightgreen'),
        ('⚡ Speed: Swerve now (conf: 0.88)', 0.15, 0.6, 'lightyellow'),
        ('🏗️ Risk: Acceptable (conf: 0.90)', 0.15, 0.5, 'lightcoral')
    ]
    
    for system, x, y, color in aligned_systems:
        ax.add_patch(FancyBboxPatch((x, y-0.03), 0.25, 0.05, 
                                   boxstyle="round,pad=0.01", facecolor=color, alpha=0.8))
        ax.text(x + 0.125, y, system, ha='center', fontsize=5.5)
    
    # Wall agreement zone
    ax.add_patch(FancyBboxPatch((0.35, 0.35), 0.4, 0.15, 
                               boxstyle="round,pad=0.02", facecolor='gold', alpha=0.6))
    ax.text(0.55, 0.42, 'WALL AGREEMENT ZONE\nAll systems perfectly aligned', 
            ha='center', fontsize=8, wrap=True)
    
    # Unified decision arrow
    ax.arrow(0.46, 0.48, 0.1, 0.05, head_width=0.03, head_length=0.03, 
             fc='green', ec='green', alpha=0.9, linewidth=3)
    ax.text(0.52, 0.52, 'SWERVE\n(High Confidence)', ha='center', fontsize=9, color='green', fontweight='bold')
    
    # Confidence indicators
    for i, (_, _, y, _) in enumerate(aligned_systems):
        ax.plot([0.4, 0.35], [y, y], 'green', linewidth=2, alpha=0.8)
    
    # Trust message
    ax.add_patch(FancyBboxPatch((0.3, 0.2), 0.4, 0.15, 
                               boxstyle="round,pad=0.02", facecolor='lightgreen', alpha=0.8))
    ax.text(0.5, 0.3, '✅ PERFECT ALIGNMENT!\nSame decision every time\nFamily knows what to expect', 
            ha='center', fontsize=8, wrap=True)
    
    # Emotional impact
    ax.text(0.5, 0.1, '😊 Family Confidence: "It will always choose to protect us"', 
            ha='center', fontsize=9, color='green', fontweight='bold')

def create_emotional_impact_comparison(ax):
    """Compare emotional impact of both cars"""
    
    ax.set_title('Family Emotional Experience Comparison', fontsize=12, fontweight='bold')
    ax.axis('off')
    
    # Traditional AI emotional timeline
    traditional_timeline = [
        ('Before Drive', '😰 Anxiety: "What if it makes wrong choice?"'),
        ('During Emergency', '😨 Panic: "Will it decide correctly this time?"'),
        ('After Safe Arrival', '😅 Relief: "That was stressful, glad we\'re okay"'),
        ('Next Time', '😰 Same Anxiety: "Will it be consistent again?"')
    ]
    
    # Wall Agreement emotional timeline
    agreement_timeline = [
        ('Before Drive', '😊 Confidence: "It will always make the right choice"'),
        ('During Emergency', '🤝 Trust: "All systems working together perfectly"'),
        ('After Safe Arrival', '😌 Peace: "Exactly what we expected, perfect protection"'),
        ('Next Time', '😊 Same Confidence: "Consistent and reliable"')
    ]
    
    # Left side - Traditional
    ax.add_patch(FancyBboxPatch((0.05, 0.8), 0.4, 0.15, 
                               boxstyle="round,pad=0.02", facecolor='lightcoral', alpha=0.6))
    ax.text(0.25, 0.9, '❌ Traditional AI Experience', ha='center', fontsize=10, fontweight='bold')
    
    y_pos = 0.75
    for time, emotion in traditional_timeline:
        ax.text(0.08, y_pos, f'{time}:', fontsize=8, fontweight='bold')
        ax.text(0.25, y_pos, emotion, fontsize=8)
        y_pos -= 0.08
    
    # Right side - Wall Agreement
    ax.add_patch(FancyBboxPatch((0.55, 0.8), 0.4, 0.15, 
                               boxstyle="round,pad=0.02", facecolor='lightgreen', alpha=0.6))
    ax.text(0.75, 0.9, '✅ Wall Agreement Experience', ha='center', fontsize=10, fontweight='bold')
    
    y_pos = 0.75
    for time, emotion in agreement_timeline:
        ax.text(0.58, y_pos, f'{time}:', fontsize=8, fontweight='bold')
        ax.text(0.75, y_pos, emotion, fontsize=8)
        y_pos -= 0.08
    
    # Emotional well-being comparison
    ax.add_patch(FancyBboxPatch((0.2, 0.1), 0.6, 0.2, 
                               boxstyle="round,pad=0.03", facecolor='gold', alpha=0.4))
    
    comparison_text = textwrap.fill(
        "The difference isn't just in the technology - it's in the family's emotional "
        "experience. Traditional AI creates ongoing anxiety and stress. Ryan's Wall "
        "Agreement creates peace of mind and trust, making autonomous vehicles a "
        "joy rather than a source of worry.",
        width=50
    )
    ax.text(0.5, 0.18, comparison_text, ha='center', fontsize=9, wrap=True)

def create_consistency_comparison(ax):
    """Show decision consistency over 100 similar emergencies"""
    
    ax.set_title('Decision Consistency: 100 Identical Emergency Scenarios', fontsize=12, fontweight='bold')
    
    scenarios = list(range(1, 101))
    
    # Traditional AI: Sometimes swerves, sometimes continues (inconsistent)
    np.random.seed(42)  # For consistent demonstration
    traditional_decisions = []
    for i in range(100):
        # 70% chance to choose "save child" but with some randomness
        if np.random.random() < 0.7:
            traditional_decisions.append(1)  # Swerve to save child
        else:
            traditional_decisions.append(0)  # Continue (hit child)
    
    # Wall Agreement: Always chooses "save child" (100% consistent)
    agreement_decisions = [1] * 100  # Always swerve to save child
    
    # Plot decisions
    ax.scatter(scenarios, traditional_decisions, c='red', alpha=0.6, s=30, 
              label='Traditional AI (Inconsistent)')
    ax.scatter(scenarios, agreement_decisions, c='green', alpha=0.6, s=30,
              label='Wall Agreement (Always Consistent)')
    
    # Add trend lines
    ax.plot(scenarios, traditional_decisions, 'red', alpha=0.3, linewidth=1)
    ax.plot(scenarios, agreement_decisions, 'green', alpha=0.8, linewidth=2)
    
    ax.set_xlabel('Emergency Scenario Number')
    ax.set_ylabel('Decision (1 = Save Child, 0 = Continue)')
    ax.set_yticks([0, 1])
    ax.set_yticklabels(['Continue\n(Hit Child)', 'Swerve\n(Save Child)'])
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Statistics
    trad_consistency = np.mean(traditional_decisions) * 100
    agreement_consistency = np.mean(agreement_decisions) * 100
    
    ax.text(50, 0.8, f'Traditional AI: {trad_consistency:.0f}% chose to save child', 
            ha='center', fontsize=9, color='red', fontweight='bold')
    ax.text(50, 0.9, f'Wall Agreement: {agreement_consistency:.0f}% chose to save child', 
            ha='center', fontsize=9, color='green', fontweight='bold')
    
    # Impact statement
    ax.text(50, -0.15, 'Consistency saves lives and builds trust.\nFamilies can rely on Wall Agreement cars every single time.', 
            ha='center', fontsize=9, transform=ax.transAxes, wrap=True)

def demonstrate_two_car_scenarios():
    """Demonstrate multiple emergency scenarios with both cars"""
    
    print("🚗 TWO CARS IN MULTIPLE EMERGENCY SCENARIOS")
    print("=" * 60)
    
    scenarios = [
        {
            'name': 'Child in Road',
            'traditional': 'Sometimes swerves (70% chance)',
            'wall_agreement': 'Always swerves to save child',
            'emotional_impact': 'Family anxiety vs peace of mind'
        },
        {
            'name': 'Sudden Obstacle',
            'traditional': 'Inconsistent braking patterns',
            'wall_agreement': 'Optimal braking every time',
            'emotional_impact': 'Unpredictable vs reliable safety'
        },
        {
            'name': 'Emergency Vehicle',
            'traditional': 'May not yield consistently',
            'wall_agreement': 'Always yields immediately',
            'emotional_impact': 'Stress vs confidence'
        },
        {
            'name': 'Pedestrian Crossing',
            'traditional': 'Variable reaction time',
            'wall_agreement': 'Immediate protective action',
            'emotional_impact': 'Worry vs trust'
        }
    ]
    
    print("\n🎯 SCENARIO COMPARISON:")
    print("-" * 50)
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\nScenario {i}: {scenario['name']}")
        print(f"  ❌ Traditional AI: {scenario['traditional']}")
        print(f"  ✅ Wall Agreement: {scenario['wall_agreement']}")
        print(f"  💝 Emotional Impact: {scenario['emotional_impact']}")
    
    print("\n" + "=" * 60)
    print("🎉 THE CRITICAL DIFFERENCE:")
    print("=" * 60)
    
    print("\n🚗 Traditional AI Car:")
    print("• Different decisions in identical situations")
    print("• Family never knows what to expect")
    print("• Creates ongoing anxiety and stress")
    print("• Trust erodes over time")
    
    print("\n🚗 Ryan's Wall Agreement Car:")
    print("• Same perfect decision every time")
    print("• Family knows exactly what to expect")
    print("• Creates peace of mind and trust")
    print("• Builds confidence over time")
    
    print("\n💝 EMOTIONAL BOTTOM LINE:")
    print("Traditional AI: 'Will it choose correctly this time?'")
    print("Wall Agreement: 'It will always protect us perfectly'")
    print("\nThat's the difference between anxiety and peace of mind!")
    print("That's the difference between stress and trust!")
    print("That's the difference between worry and confidence!")

if __name__ == "__main__":
    create_two_cars_comparison()
    demonstrate_two_car_scenarios()
    
    print("\n" + "="*70)
    print("🎉 TWO CARS COMPARISON VISUALIZATION COMPLETE!")
    print("="*70)
    print("\n📖 WHAT YOUR FAMILY WILL SEE:")
    print("• Same emergency, two different cars side-by-side")
    print("• Traditional AI: Systems disagree, inconsistent decisions")
    print("• Ryan's Car: Perfect alignment, consistent protection")
    print("• Real emotional impact comparison")
    print("• Why consistency matters for family safety")
    print("\n🚗 PERFECT FOR FAMILY DISCUSSIONS:")
    print("• 'Look at both cars in the same situation!'")
    print("• 'Which car would you rather be in?'")
    print("• 'Ryan made the car that always chooses to protect!'")
    print("• 'Now we can trust autonomous vehicles!'")
    print("\n💝 THE EMOTIONAL IMPACT:")
    print("This shows the real human difference - turning fear into trust,")
    print("anxiety into peace of mind, and uncertainty into confidence!")
