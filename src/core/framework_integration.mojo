from core.cognitive_adaptation import CognitiveAdaptationSystem
from core.performance_optimization import PerformanceOptimizationSystem
from core.safety_validation import MemorySafetySystem
from core.interfaces.cognitive_bridge import InterfaceBridgingSystem
from collections import Dict

# Add a dictionary type
alias PerformanceMetrics = Dict[String, Float64]

struct IntelligentCognitiveFramework:
    var cognitive_adaptation: CognitiveAdaptationSystem
    var performance_optimization: PerformanceOptimizationSystem
    var memory_safety: MemorySafetySystem
    var interface_bridging: InterfaceBridgingSystem

    fn __init__(inout self):
        self.cognitive_adaptation = CognitiveAdaptationSystem()
        self.performance_optimization = PerformanceOptimizationSystem()
        self.memory_safety = MemorySafetySystem()
        self.interface_bridging = InterfaceBridgingSystem()

    fn process_cognitive_task[T: AnyType](
        inout self, 
        input: T, 
        complexity: Float64
    ) -> T:
        """
        Holistic intelligent processing of cognitive tasks.
        """
        var validated_input = self.memory_safety.mitigate_risk(input)
        var adapted_input = self.cognitive_adaptation.dynamically_adjust_complexity(
            validated_input, complexity
        )
        var optimized_input = self.performance_optimization.optimize_computational_strategy(
            adapted_input, complexity
        )
        
        return optimized_input

    fn reset_framework(inout self):
        """
        Reset all subsystems for a new learning cycle.
        """
        self.cognitive_adaptation.reset_complexity_tracking()
        self.performance_optimization.reset_performance_tracking()
        self.memory_safety.reset_safety_tracking()

    fn analyze_framework_performance(self) -> PerformanceMetrics:
        """
        Generate a comprehensive performance analysis.
        """
        var performance_metrics = PerformanceMetrics()
        
        performance_metrics["cognitive_complexity_trend"] = (
            self.cognitive_adaptation.compute_complexity_trend()
        )
        performance_metrics["computational_efficiency"] = (
            self.performance_optimization.analyze_performance_trend()
        )
        
        return performance_metrics 