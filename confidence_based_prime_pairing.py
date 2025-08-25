#!/usr/bin/env python3
"""
Confidence-Based Prime Pairing System
Evolution from linear pairing to consciousness-representative pairing

This system incorporates confidence measures into twin prime pairing to better
represent human consciousness over time, moving beyond simple linear progression.
"""

import math
import random
from typing import Dict, List, Tuple, Optional
from datetime import datetime

class ConfidenceBasedPrimePairing:
    """Confidence-based prime pairing that represents consciousness over time"""
    
    def __init__(self, max_primes: int = 1000):
        self.max_primes = max_primes
        self.prime_confidence_map = {}
        self.temporal_memory = {}
        self.attention_weights = {}
        self.emotional_resonance = {}
        
        # Initialize confidence tracking for primes
        self.initialize_prime_confidence_system()
    
    def initialize_prime_confidence_system(self):
        """Initialize the confidence-based system for prime awareness"""
        primes = self.generate_primes_up_to(self.max_primes)
        
        for prime in primes:
            # Base confidence from mathematical properties
            base_confidence = self.calculate_prime_mathematical_confidence(prime)
            
            # Temporal accessibility (consciousness-like memory)
            temporal_accessibility = self.calculate_temporal_accessibility(prime)
            
            # Attention weight (focus/importance)
            attention_weight = self.calculate_attention_weight(prime)
            
            # Emotional resonance (cognitive significance)
            emotional_resonance = self.calculate_emotional_resonance(prime)
            
            self.prime_confidence_map[prime] = {
                'mathematical_confidence': base_confidence,
                'temporal_accessibility': temporal_accessibility,
                'attention_weight': attention_weight,
                'emotional_resonance': emotional_resonance,
                'overall_confidence': self.compute_overall_confidence(
                    base_confidence, temporal_accessibility, attention_weight, emotional_resonance
                )
            }
    
    def calculate_prime_mathematical_confidence(self, prime: int) -> float:
        """Calculate confidence based on prime's mathematical properties"""
        # Confidence increases with prime size (larger primes are "more confident")
        size_confidence = min(1.0, math.log(prime) / math.log(1000))
        
        # Twin prime confidence (higher for twin primes)
        is_twin = self.is_twin_prime(prime)
        twin_confidence = 0.9 if is_twin else 0.3
        
        # Prime gap confidence (smaller gaps = higher confidence)
        gap_confidence = self.calculate_gap_confidence(prime)
        
        return (size_confidence * 0.3 + twin_confidence * 0.4 + gap_confidence * 0.3)
    
    def calculate_temporal_accessibility(self, prime: int) -> float:
        """Calculate how accessible this prime is in consciousness over time"""
        # Recent primes are more accessible (recency effect)
        recency_factor = 1.0 / (1.0 + math.log(prime))
        
        # Frequency effect (primes that appear in important contexts)
        frequency_factor = self.calculate_frequency_factor(prime)
        
        # Priming effect (related primes boost accessibility)
        priming_factor = self.calculate_priming_factor(prime)
        
        return min(1.0, recency_factor * frequency_factor * priming_factor)
    
    def calculate_attention_weight(self, prime: int) -> float:
        """Calculate attention weight (conscious focus)"""
        # Attention follows an inverted U-shape (optimal around certain primes)
        optimal_attention_prime = 100
        attention_curve = 1.0 / (1.0 + ((prime - optimal_attention_prime) / 50.0)**2)
        
        # Novelty bonus (new/interesting primes get more attention)
        novelty_bonus = self.calculate_novelty_bonus(prime)
        
        return min(1.0, attention_curve * novelty_bonus)
    
    def calculate_emotional_resonance(self, prime: int) -> float:
        """Calculate emotional/cognitive significance"""
        # Some primes resonate more emotionally/cognitively
        resonance_patterns = [7, 11, 13, 17, 23, 29, 31, 37, 41, 43, 47, 53]
        if prime in resonance_patterns:
            base_resonance = 0.9
        else:
            base_resonance = 0.4
        
        # Emotional decay over time (consciousness fades)
        emotional_decay = 1.0 / (1.0 + math.log(prime) * 0.1)
        
        return base_resonance * emotional_decay
    
    def compute_overall_confidence(self, math_conf, temporal_acc, attention_wt, emotional_res) -> float:
        """Compute overall confidence from all factors"""
        # Weighted combination representing consciousness integration
        weights = {
            'mathematical': 0.25,
            'temporal': 0.30,
            'attention': 0.25,
            'emotional': 0.20
        }
        
        overall = (
            math_conf * weights['mathematical'] +
            temporal_acc * weights['temporal'] +
            attention_wt * weights['attention'] +
            emotional_res * weights['emotional']
        )
        
        return min(1.0, max(0.0, overall))
    
    def generate_confidence_based_pairs(self, num_pairs: int = 10) -> List[Tuple[int, int, float]]:
        """Generate prime pairs based on confidence measures, not linear progression"""
        pairs_with_confidence = []
        
        primes = list(self.prime_confidence_map.keys())
        primes.sort(key=lambda p: self.prime_confidence_map[p]['overall_confidence'], reverse=True)
        
        # Create pairs based on confidence similarity and consciousness associations
        for i in range(min(num_pairs, len(primes) - 1)):
            current_prime = primes[i]
            
            # Find best pair based on confidence compatibility, not just next prime
            best_pair = self.find_best_confidence_pair(current_prime, primes[i+1:])
            
            if best_pair:
                pair_confidence = self.calculate_pair_confidence(current_prime, best_pair)
                pairs_with_confidence.append((current_prime, best_pair, pair_confidence))
        
        return pairs_with_confidence
    
    def find_best_confidence_pair(self, prime: int, candidates: List[int]) -> int:
        """Find the best pair for a prime based on confidence compatibility"""
        best_candidate = None
        best_score = 0.0
        
        current_confidence = self.prime_confidence_map[prime]['overall_confidence']
        
        for candidate in candidates:
            candidate_confidence = self.prime_confidence_map[candidate]['overall_confidence']
            
            # Confidence compatibility score
            confidence_compatibility = 1.0 - abs(current_confidence - candidate_confidence)
            
            # Consciousness association score (temporal + emotional)
            temporal_assoc = min(
                self.prime_confidence_map[prime]['temporal_accessibility'],
                self.prime_confidence_map[candidate]['temporal_accessibility']
            )
            
            emotional_assoc = min(
                self.prime_confidence_map[prime]['emotional_resonance'],
                self.prime_confidence_map[candidate]['emotional_resonance']
            )
            
            # Mathematical association (prime properties)
            math_distance = abs(prime - candidate)
            math_assoc = 1.0 / (1.0 + math_distance / 10.0)
            
            # Combined score
            total_score = (
                confidence_compatibility * 0.4 +
                temporal_assoc * 0.3 +
                emotional_assoc * 0.2 +
                math_assoc * 0.1
            )
            
            if total_score > best_score:
                best_score = total_score
                best_candidate = candidate
        
        return best_candidate
    
    def calculate_pair_confidence(self, prime1: int, prime2: int) -> float:
        """Calculate confidence of a prime pair"""
        conf1 = self.prime_confidence_map[prime1]['overall_confidence']
        conf2 = self.prime_confidence_map[prime2]['overall_confidence']
        
        # Pair confidence is geometric mean of individual confidences
        # plus association bonus
        association_bonus = self.calculate_association_bonus(prime1, prime2)
        
        return min(1.0, math.sqrt(conf1 * conf2) + association_bonus)
    
    def calculate_association_bonus(self, prime1: int, prime2: int) -> float:
        """Calculate bonus for strong prime associations"""
        # Twin prime bonus
        if abs(prime1 - prime2) == 2:
            return 0.3
        
        # Resonance pattern bonus
        resonance_patterns = [
            (7, 11), (11, 13), (13, 17), (17, 23), (23, 29),
            (29, 31), (31, 37), (37, 41), (41, 43), (43, 47)
        ]
        
        for p1, p2 in resonance_patterns:
            if (prime1 == p1 and prime2 == p2) or (prime1 == p2 and prime2 == p1):
                return 0.2
        
        return 0.0
    
    # Helper methods
    def generate_primes_up_to(self, n: int) -> List[int]:
        """Generate primes up to n using sieve"""
        sieve = [True] * (n + 1)
        sieve[0] = sieve[1] = False
        
        for i in range(2, int(math.sqrt(n)) + 1):
            if sieve[i]:
                for j in range(i*i, n+1, i):
                    sieve[j] = False
        
        return [i for i in range(2, n+1) if sieve[i]]
    
    def is_twin_prime(self, prime: int) -> bool:
        """Check if prime is part of a twin prime pair"""
        primes = list(self.prime_confidence_map.keys())
        return (prime + 2 in primes) or (prime - 2 in primes)
    
    def calculate_gap_confidence(self, prime: int) -> float:
        """Calculate confidence based on prime gap"""
        next_prime = self.find_next_prime(prime)
        if next_prime:
            gap = next_prime - prime
            # Smaller gaps = higher confidence
            return max(0.1, 1.0 / (1.0 + gap / 10.0))
        return 0.5
    
    def find_next_prime(self, prime: int) -> int:
        """Find next prime after given prime"""
        primes = list(self.prime_confidence_map.keys())
        primes.sort()
        
        for p in primes:
            if p > prime:
                return p
        return None
    
    def calculate_frequency_factor(self, prime: int) -> float:
        """Calculate how frequently this prime appears in consciousness"""
        # Smaller primes appear more frequently in mathematical contexts
        return 1.0 / (1.0 + math.log(prime) * 0.5)
    
    def calculate_priming_factor(self, prime: int) -> float:
        """Calculate priming effect from related primes"""
        # Primed by factors and multiples
        priming_score = 0.0
        
        for p in self.prime_confidence_map:
            if p != prime and (prime % p == 0 or p % prime == 0):
                priming_score += 0.1
        
        return min(1.0, 0.5 + priming_score)
    
    def calculate_novelty_bonus(self, prime: int) -> float:
        """Calculate novelty bonus for attention"""
        # Novel primes get attention bonus
        if prime in [2, 3, 5, 7, 11, 13]:  # Well-known primes
            return 0.7
        elif prime < 100:  # Moderately known
            return 1.0
        else:  # Large primes - more novel
            return 1.2


class ConsciousnessInspiredPrimeDemonstrator:
    """Demonstrate the difference between linear and confidence-based pairing"""
    
    def __init__(self):
        self.confidence_pairing = ConfidenceBasedPrimePairing()
    
    def compare_pairing_approaches(self):
        """Compare linear vs confidence-based pairing approaches"""
        print("🧠 CONSCIOUSNESS-INSPIRED PRIME PAIRING ANALYSIS")
        print("=" * 80)
        
        # Traditional linear pairing
        print("\n📏 TRADITIONAL LINEAR PAIRING:")
        print("Based on mathematical sequence, not consciousness dynamics")
        linear_pairs = [
            (3, 5), (5, 7), (11, 13), (17, 19), (29, 31),
            (41, 43), (59, 61), (71, 73), (101, 103), (107, 109)
        ]
        
        for i, (p1, p2) in enumerate(linear_pairs[:5]):
            print(f"  Pair {i+1}: ({p1}, {p2}) - Sequential progression")
        
        # Confidence-based pairing
        print("\n🧠 CONSCIOUSNESS-BASED PAIRING:")
        print("Based on confidence measures and cognitive associations")
        confidence_pairs = self.confidence_pairing.generate_confidence_based_pairs(10)
        
        for i, (p1, p2, conf) in enumerate(confidence_pairs):
            pair_type = self.analyze_pair_characteristics(p1, p2)
            print(f"  Pair {i+1}: ({p1}, {p2}) - Confidence: {conf:.3f} - {pair_type}")
        
        # Show confidence evolution
        self.visualize_confidence_evolution(confidence_pairs)
        
        # Analyze consciousness representation
        self.analyze_consciousness_representation(linear_pairs, confidence_pairs)
    
    def analyze_pair_characteristics(self, p1: int, p2: int) -> str:
        """Analyze what makes this pair special"""
        if abs(p1 - p2) == 2:
            return "Twin Prime (Mathematical)"
        elif abs(p1 - p2) < 10:
            return "Close Association"
        elif p1 in [7, 11, 13] and p2 in [17, 23, 29]:
            return "Resonance Pattern"
        elif abs(p1 - p2) > 50:
            return "Distant Association"
        else:
            return "Confidence Compatible"
    
    def visualize_confidence_evolution(self, confidence_pairs):
        """Visualize how confidence evolves in the pairing system"""
        print("\n📊 CONFIDENCE EVOLUTION ANALYSIS:")
        
        primes_shown = []
        confidences_shown = []
        
        for i, (p1, p2, conf) in enumerate(confidence_pairs[:8]):
            primes_shown.extend([p1, p2])
            confidences_shown.extend([
                self.confidence_pairing.prime_confidence_map[p1]['overall_confidence'],
                self.confidence_pairing.prime_confidence_map[p2]['overall_confidence']
            ])
        
        # Show confidence progression
        print("  Prime Confidence Evolution:")
        for i in range(0, len(primes_shown), 2):
            if i + 1 < len(primes_shown):
                p1, p2 = primes_shown[i], primes_shown[i+1]
                c1, c2 = confidences_shown[i], confidences_shown[i+1]
                pair_conf = confidence_pairs[i//2][2]
                print(f"    ({p1}: {c1:.3f}, {p2}: {c2:.3f}) → Pair confidence: {pair_conf:.3f}")
    
    def analyze_consciousness_representation(self, linear_pairs, confidence_pairs):
        """Analyze how well each approach represents consciousness"""
        print("\n🧠 CONSCIOUSNESS REPRESENTATION ANALYSIS:")
        print("=" * 60)
        
        print("\n📏 LINEAR PAIRING LIMITATIONS:")
        limitations = [
            "Sequential processing (not parallel consciousness)",
            "No memory/recall dynamics",
            "No attention weighting",
            "No emotional resonance",
            "No confidence measures",
            "Doesn't represent human cognition over time"
        ]
        
        for limitation in limitations:
            print(f"  ❌ {limitation}")
        
        print("\n🧠 CONSCIOUSNESS-BASED PAIRING FEATURES:")
        features = [
            "Confidence-driven associations",
            "Temporal accessibility modeling",
            "Attention weighting system",
            "Emotional resonance patterns",
            "Memory and recall dynamics",
            "Non-linear cognitive connections"
        ]
        
        for feature in features:
            print(f"  ✅ {feature}")
        
        print("\n🎯 KEY INSIGHT:")
        print("  Linear pairing: Mathematical sequence")
        print("  Confidence pairing: Human consciousness dynamics")
        print("  This represents the evolution from algorithm to cognition!")
    
    def demonstrate_confidence_driven_cognition(self):
        """Demonstrate how confidence drives cognitive-like behavior"""
        print("\n🧠 CONFIDENCE-DRIVEN COGNITION DEMONSTRATION:")
        print("=" * 60)
        
        # Show top confidence primes
        primes_by_confidence = sorted(
            self.confidence_pairing.prime_confidence_map.items(),
            key=lambda x: x[1]['overall_confidence'],
            reverse=True
        )
        
        print("\n🔝 TOP 10 MOST CONFIDENT PRIMES:")
        for i, (prime, data) in enumerate(primes_by_confidence[:10]):
            print(f"  {i+1:2d}. Prime {prime:3d}: Confidence {data['overall_confidence']:.3f}")
        
        # Show confidence factors for a specific prime
        example_prime = 41
        if example_prime in self.confidence_pairing.prime_confidence_map:
            data = self.confidence_pairing.prime_confidence_map[example_prime]
            print(f"\n🔍 CONFIDENCE BREAKDOWN FOR PRIME {example_prime}:")
            print(f"  Mathematical confidence: {data['mathematical_confidence']:.3f}")
            print(f"  Temporal accessibility:   {data['temporal_accessibility']:.3f}")
            print(f"  Attention weight:        {data['attention_weight']:.3f}")
            print(f"  Emotional resonance:     {data['emotional_resonance']:.3f}")
            print(f"  Overall confidence:      {data['overall_confidence']:.3f}")
        
        # Show how confidence affects pairing
        print("\n🔗 CONFIDENCE-BASED PAIRING LOGIC:")
        print("  1. Sort primes by overall confidence")
        print("  2. For each prime, find best confidence-compatible pair")
        print("  3. Consider temporal, emotional, and mathematical factors")
        print("  4. Create associations that represent consciousness, not just math")


def main():
    """Main demonstration function"""
    print("🧠 CONSCIOUSNESS-INSPIRED PRIME PAIRING SYSTEM")
    print("Evolution from Linear to Confidence-Based Pairing")
    print("=" * 80)
    
    # Create the consciousness-inspired demonstrator
    consciousness_demo = ConsciousnessInspiredPrimeDemonstrator()
    
    # Compare the two approaches
    consciousness_demo.compare_pairing_approaches()
    
    # Demonstrate confidence-driven cognition
    consciousness_demo.demonstrate_confidence_driven_cognition()
    
    print("\n🎯 CONCLUSION:")
    print("This confidence-based approach transforms prime pairing from")
    print("mathematical sequence to human consciousness representation!")
    print("\nThe system now incorporates:")
    print("• Confidence measures for each prime")
    print("• Temporal accessibility (memory)")
    print("• Attention weighting (focus)")
    print("• Emotional resonance (significance)")
    print("• Non-linear associations (consciousness)")


if __name__ == "__main__":
    main()
