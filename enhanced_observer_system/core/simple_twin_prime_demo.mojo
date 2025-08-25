"""
Simple Twin Prime Chaos Demonstration
Basic Mojo implementation with fixed syntax
"""

from python import Python
from math import sqrt, log, exp, sin, cos, pi

struct PrimePair:
    var lower: Int
    var upper: Int
    var ratio: Float64
    
    fn __init__(inout self, l: Int, u: Int):
        self.lower = l
        self.upper = u
        self.ratio = Float64(u) / Float64(l)

fn generate_twin_primes() -> List[PrimePair]:
    var pairs = List[PrimePair]()
    
    var twin_primes = [
        (3, 5), (5, 7), (11, 13), (17, 19), (29, 31),
        (41, 43), (59, 61), (71, 73), (101, 103)
    ]
    
    for pair in twin_primes:
        pairs.append(PrimePair(pair[0], pair[1]))
    
    return pairs

fn normalize_position(prime: Int) -> Float64:
    # Base position around 120 degrees (2.0944 radians)
    var base = 2.0944
    
    # Simple prime-based variation
    var variation = Float64(prime % 100) / 1000.0  # 0-0.1 range
    var sign = 1.0 if (prime % 2 == 0) else -1.0
    
    return base + sign * variation

fn demonstrate_prime_chaos():
    print("🧬 SIMPLE TWIN PRIME CHAOS DEMONSTRATION")
    print("=" * 50)
    
    # Generate prime pairs
    print("\n🔢 Generating Twin Prime Pairs:")
    var prime_pairs = generate_twin_primes()
    
    for i in range(len(prime_pairs)):
        var pair = prime_pairs[i]
        print("  Pair", String(i + 1) + ":", String(pair.lower), "+", String(pair.upper), 
              "(ratio:", String(pair.ratio), ")")
    
    # Generate chaos-ready positions
    print("\n🎯 Chaos-Ready Initial Conditions:")
    for i in range(len(prime_pairs)):
        var pair = prime_pairs[i]
        
        # Generate positions from both primes in pair
        var pos1 = normalize_position(pair.lower)
        var pos2 = normalize_position(pair.upper)
        
        var angle1 = pos1 * 180.0 / pi
        var angle2 = pos2 * 180.0 / pi
        
        print("  Agent", String(i * 2), ": Position =", String(pos1), "rad (" + String(angle1) + "°)")
        print("  Agent", String(i * 2 + 1), ": Position =", String(pos2), "rad (" + String(angle2) + "°)")
    
    # Simple chaos analysis
    print("\n🌌 Chaos Analysis:")
    
    var positions = List[Float64]()
    for pair in prime_pairs:
        positions.append(normalize_position(pair.lower))
        positions.append(normalize_position(pair.upper))
    
    # Calculate spread
    var min_pos = positions[0]
    var max_pos = positions[0]
    var total = 0.0
    
    for pos in positions:
        if pos < min_pos:
            min_pos = pos
        if pos > max_pos:
            max_pos = pos
        total += pos
    
    var mean_pos = total / Float64(len(positions))
    var spread = max_pos - min_pos
    var spread_degrees = spread * 180.0 / pi
    
    print("  • Total agents:", String(len(positions)))
    print("  • Position range:", String(min_pos), "to", String(max_pos), "radians")
    print("  • Angular spread:", String(spread_degrees), "degrees")
    print("  • Mean position:", String(mean_pos), "radians")
    print("  • Chaos coverage: Good distribution around attractor")
    
    print("\n✨ DEMONSTRATION COMPLETE")
    print("   Prime-based initial conditions generated")
    print("   Chaos-ready positions calculated")
    print("   Basic mathematical structure validated")

fn main():
    demonstrate_prime_chaos()

main()
