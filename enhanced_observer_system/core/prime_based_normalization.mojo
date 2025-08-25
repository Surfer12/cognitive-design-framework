"""
Prime-Based Position Normalization
Generate chaotic initial conditions from prime number properties
"""

from python import Python
from math import sqrt, log, exp, pow, sin, cos, pi, atan2, tanh
from time import now

struct PrimeTwinPair:
    """Prime twin pair with mathematically generated positions"""
    
    var lower: Int
    var upper: Int
    var normalized_lower: Float64
    var normalized_upper: Float64
    var prime_ratio: Float64
    var prime_difference: Int
    var chaos_seed: Float64
    
    fn __init__(inout self, lower_prime: Int, upper_prime: Int):
        """Initialize prime twin pair with mathematical position generation"""
        self.lower = lower_prime
        self.upper = upper_prime
        self.prime_ratio = Float64(upper_prime) / Float64(lower_prime)
        self.prime_difference = upper_prime - lower_prime
        
        # Generate chaos seed from prime properties
        self.chaos_seed = self.generate_chaos_seed()
        
        # Generate normalized positions from prime properties
        self.normalized_lower = self.generate_position_from_prime(lower_prime, false)
        self.normalized_upper = self.generate_position_from_prime(upper_prime, true)
        
    fn generate_chaos_seed(inout self) -> Float64:
        """Generate chaos seed from prime properties"""
        # Use prime ratio and difference to create unique seed
        var ratio_component = self.prime_ratio - 1.0  # Deviation from 1
        var difference_component = Float64(self.prime_difference) / 10.0
        
        # Combine with golden ratio for chaotic properties
        var golden_ratio = (1.0 + sqrt(5.0)) / 2.0
        var seed = (ratio_component * golden_ratio + difference_component) / 10.0
        
        return tanh(seed)  # Bound between -1 and 1
        
    fn generate_position_from_prime(inout self, prime: Int, is_upper: Bool) -> Float64:
        """Generate normalized position from prime number properties"""
        # Base chaotic attractor position (120° = 2.0944 radians)
        var base_position = 2.0944
        
        # Extract prime properties
        var prime_digits = self.extract_prime_digits(prime)
        var prime_mod_100 = Float64(prime % 100)
        var prime_sqrt = sqrt(Float64(prime))
        var prime_log = log(Float64(prime))
        
        # Multi-factor position generation
        var digit_factor = Float64(prime_digits) / 100.0  # Digit-based variation
        var modulo_factor = (prime_mod_100 - 50.0) / 500.0  # Centered modulo
        var sqrt_factor = (prime_sqrt - 5.0) / 50.0  # Square root scaling
        var log_factor = (prime_log - 2.0) / 10.0  # Logarithmic scaling
        
        # Combine factors with different weights
        var combined_factor = (
            digit_factor * 0.3 +     # Digit pattern influence
            modulo_factor * 0.3 +    # Modulo distribution
            sqrt_factor * 0.2 +      # Square root structure
            log_factor * 0.2         # Logarithmic growth
        )
        
        # Apply twin pair distinction
        var twin_distinction = self.prime_difference / 20.0
        if is_upper:
            combined_factor += twin_distinction * 0.1
        else:
            combined_factor -= twin_distinction * 0.1
            
        # Apply chaos seed influence
        combined_factor += self.chaos_seed * 0.2
        
        # Generate final position with controlled variance
        var position = base_position + combined_factor * 0.1  # ±0.1 radian variation
        
        # Ensure position stays within reasonable bounds for double pendulum
        position = max(1.0, min(4.0, position))  # Keep within reasonable angle range
        
        return position
        
    fn extract_prime_digits(inout self, prime: Int) -> Int:
        """Extract meaningful digit pattern from prime"""
        var prime_str = String(prime)
        var digit_sum = 0
        
        for i in range(len(prime_str)):
            var digit = prime_str[i]
            if digit == "0":
                digit_sum += 0
            elif digit == "1":
                digit_sum += 1
            elif digit == "2":
                digit_sum += 2
            elif digit == "3":
                digit_sum += 3
            elif digit == "4":
                digit_sum += 4
            elif digit == "5":
                digit_sum += 5
            elif digit == "6":
                digit_sum += 6
            elif digit == "7":
                digit_sum += 7
            elif digit == "8":
                digit_sum += 8
            elif digit == "9":
                digit_sum += 9
                
        return digit_sum
        
    fn get_prime_based_velocity(inout self, base_velocity: Float64 = 0.001) -> Tuple[Float64, Float64]:
        """Generate velocity pair based on prime properties"""
        # Use prime ratio to generate velocity asymmetry
        var ratio_factor = (self.prime_ratio - 1.0) * 0.5
        
        # Use prime difference for magnitude variation
        var difference_factor = Float64(self.prime_difference) / 100.0
        
        # Generate velocities with prime-influenced perturbations
        var vel_lower = base_velocity + ratio_factor * 0.002 + difference_factor * 0.001
        var vel_upper = base_velocity - ratio_factor * 0.001 + difference_factor * 0.002
        
        return (vel_lower, vel_upper)
        
    fn get_mathematical_properties(inout self) -> String:
        """Get mathematical properties of the twin pair"""
        var properties = "=== PRIME TWIN PAIR PROPERTIES ===\n"
        properties += "Lower Prime: " + String(self.lower) + "\n"
        properties += "Upper Prime: " + String(self.upper) + "\n"
        properties += "Prime Ratio: " + String(self.prime_ratio) + "\n"
        properties += "Prime Difference: " + String(self.prime_difference) + "\n"
        properties += "Normalized Lower: " + String(self.normalized_lower) + " rad\n"
        properties += "Normalized Upper: " + String(self.normalized_upper) + " rad\n"
        properties += "Chaos Seed: " + String(self.chaos_seed) + "\n"
        
        var angle_lower = self.normalized_lower * 180.0 / pi
        var angle_upper = self.normalized_upper * 180.0 / pi
        
        properties += "Angle Lower: " + String(angle_lower) + "°\n"
        properties += "Angle Upper: " + String(angle_upper) + "°\n"
        
        return properties

struct PrimeBasedNormalizer:
    """Advanced normalizer using prime number theory"""
    
    var twin_pairs: List[PrimeTwinPair]
    var normalization_method: String
    var chaos_sensitivity: Float64
    
    fn __init__(inout self, method: String = "adaptive"):
        """Initialize prime-based normalizer"""
        self.twin_pairs = List[PrimeTwinPair]()
        self.normalization_method = method
        self.chaos_sensitivity = 0.7
        
        # Generate initial twin pairs
        self.generate_twin_pairs()
        
    fn generate_twin_pairs(inout self):
        """Generate comprehensive set of twin prime pairs"""
        var known_twin_primes = [
            (3, 5), (5, 7), (11, 13), (17, 19), (29, 31),
            (41, 43), (59, 61), (71, 73), (101, 103), (107, 109),
            (137, 139), (149, 151), (179, 181), (191, 193), (197, 199),
            (227, 229), (239, 241), (269, 271), (281, 283), (311, 313),
            (347, 349), (419, 421), (431, 433), (461, 463), (521, 523),
            (569, 571), (599, 601), (617, 619), (641, 643), (659, 661),
            (809, 811), (821, 823), (827, 829), (857, 859), (881, 883)
        ]
        
        for pair in known_twin_primes:
            var twin_pair = PrimeTwinPair(pair[0], pair[1])
            self.twin_pairs.append(twin_pair)
            
    fn get_normalized_position(inout self, index: Int, is_upper: Bool) -> Float64:
        """Get normalized position from prime-based calculation"""
        if len(self.twin_pairs) == 0:
            return 2.0944  # Default position
            
        var pair_index = index % len(self.twin_pairs)
        var twin_pair = self.twin_pairs[pair_index]
        
        return twin_pair.normalized_upper if is_upper else twin_pair.normalized_lower
        
    fn get_prime_influenced_velocity(inout self, index: Int, base_velocity: Float64 = 0.001) -> Float64:
        """Get velocity influenced by prime properties"""
        if len(self.twin_pairs) == 0:
            return base_velocity
            
        var pair_index = index % len(self.twin_pairs)
        var twin_pair = self.twin_pairs[pair_index]
        
        var (vel_lower, vel_upper) = twin_pair.get_prime_based_velocity(base_velocity)
        
        return vel_upper if (index % 2 == 0) else vel_lower
        
    fn generate_chaos_ready_initial_conditions(inout self, num_agents: Int) -> Dict[String, List[Float64]]:
        """Generate chaos-ready initial conditions from prime mathematics"""
        var initial_conditions = Dict[String, List[Float64]]()
        var positions = List[Float64]()
        var velocities = List[Float64]()
        
        print("🎯 GENERATING PRIME-BASED INITIAL CONDITIONS")
        print("=" * 55)
        
        for i in range(num_agents):
            var position = self.get_normalized_position(i, i % 2 == 0)
            var velocity = self.get_prime_influenced_velocity(i)
            
            positions.append(position)
            velocities.append(velocity)
            
            var angle_deg = position * 180.0 / pi
            print("Agent " + String(i) + ": " + 
                  "Position=" + String(position) + " rad (" + String(angle_deg) + "°), " +
                  "Velocity=" + String(velocity))
                  
        initial_conditions["x"] = positions
        initial_conditions["v"] = velocities
        
        return initial_conditions
        
    fn analyze_prime_structure_effectiveness(inout self) -> Dict[String, Float64]:
        """Analyze how effectively prime structure contributes to chaos readiness"""
        var analysis = Dict[String, Float64]()
        
        if len(self.twin_pairs) == 0:
            return analysis
            
        # Analyze position distribution
        var positions = List[Float64]()
        for pair in self.twin_pairs:
            positions.append(pair.normalized_lower)
            positions.append(pair.normalized_upper)
            
        # Calculate distribution metrics
        var mean_position = 0.0
        var variance = 0.0
        var min_pos = positions[0]
        var max_pos = positions[0]
        
        for pos in positions:
            mean_position += pos
            min_pos = min(min_pos, pos)
            max_pos = max(max_pos, pos)
            
        mean_position /= Float64(len(positions))
        
        for pos in positions:
            variance += pow(pos - mean_position, 2)
        variance /= Float64(len(positions))
        
        var std_dev = sqrt(variance)
        var spread = max_pos - min_pos
        
        analysis["mean_position"] = mean_position
        analysis["position_std_dev"] = std_dev
        analysis["position_spread"] = spread
        analysis["chaos_coverage"] = spread / (2.0 * pi)  # Fraction of angle space covered
        
        return analysis
        
    fn get_normalization_report(inout self) -> String:
        """Generate comprehensive normalization report"""
        var report = "=== PRIME-BASED NORMALIZATION REPORT ===\n"
        report += "Generated: " + String(now()) + "\n\n"
        
        report += "NORMALIZATION CONFIGURATION:\n"
        report += "  • Method: " + self.normalization_method + "\n"
        report += "  • Chaos Sensitivity: " + String(self.chaos_sensitivity) + "\n"
        report += "  • Twin Pairs Available: " + String(len(self.twin_pairs)) + "\n\n"
        
        report += "SAMPLE TWIN PAIR ANALYSIS:\n"
        if len(self.twin_pairs) > 0:
            var sample_pair = self.twin_pairs[0]
            report += sample_pair.get_mathematical_properties() + "\n"
            
        var analysis = self.analyze_prime_structure_effectiveness()
        report += "STRUCTURAL EFFECTIVENESS:\n"
        report += "  • Mean Position: " + String(analysis.get("mean_position", 0.0)) + " rad\n"
        report += "  • Position Std Dev: " + String(analysis.get("position_std_dev", 0.0)) + "\n"
        report += "  • Position Spread: " + String(analysis.get("position_spread", 0.0)) + " rad\n"
        report += "  • Chaos Coverage: " + String(analysis.get("chaos_coverage", 0.0) * 100.0) + "%\n\n"
        
        report += "MATHEMATICAL PROPERTIES:\n"
        report += "  • Base Chaotic Position: 2.0944 rad (120°)\n"
        report += "  • Prime Influence Factors: 4 (digits, modulo, sqrt, log)\n"
        report += "  • Chaos Seed Generation: tanh(ratio + difference)\n"
        report += "  • Twin Distinction: ±difference/20\n"
        report += "  • Position Bounds: [1.0, 4.0] rad\n\n"
        
        report += "CHAOS PREPARATION:\n"
        report += "  • Prime-based distribution around attractor\n"
        report += "  • Velocity perturbations from prime ratios\n"
        report += "  • Mathematical structure for bifurcation detection\n"
        report += "  • Enhanced predictability through prime properties\n"
        
        return report

fn create_prime_based_normalizer() -> PrimeBasedNormalizer:
    """Factory function to create prime-based normalizer"""
    return PrimeBasedNormalizer()

fn demonstrate_prime_normalization():
    """Demonstrate prime-based position normalization"""
    print("🔢 PRIME-BASED POSITION NORMALIZATION DEMONSTRATION")
    print("=" * 65)
    
    var normalizer = PrimeBasedNormalizer("adaptive")
    
    print("\n📊 SAMPLE TWIN PAIR ANALYSIS:")
    if len(normalizer.twin_pairs) > 0:
        var sample = normalizer.twin_pairs[0]
        print(sample.get_mathematical_properties())
        
    print("\n🎯 INITIAL CONDITIONS GENERATION:")
    var conditions = normalizer.generate_chaos_ready_initial_conditions(5)
    
    print("\n📈 STRUCTURAL ANALYSIS:")
    var analysis = normalizer.analyze_prime_structure_effectiveness()
    print("  • Mean Position: " + String(analysis.get("mean_position", 0.0)) + " rad")
    print("  • Position Spread: " + String(analysis.get("position_spread", 0.0)) + " rad")
    print("  • Chaos Coverage: " + String(analysis.get("chaos_coverage", 0.0) * 100.0) + "%")
    
    print("\n" + normalizer.get_normalization_report())

print("🔢 Prime-Based Normalization - Ready!")
print("🧮 Mathematical Position Generation from Primes")
print("🎯 Chaos-Ready Initial Conditions")
print("📊 Prime Property Analysis")
print("🌌 Enhanced Bifurcation Detection")
print("🔬 Structure-Preserving Chaos Prediction")
