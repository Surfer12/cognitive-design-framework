from src.core.framework_integration import IntelligentCognitiveFramework

fn process_complex_data[T: AnyType](input: T, complexity: Float64) -> T:
    """
    Demonstrate cognitive framework processing.
    """
    var cognitive_framework = IntelligentCognitiveFramework()
    
    # Process input through intelligent framework
    var processed_input = cognitive_framework.process_cognitive_task(input, complexity)
    
    # Analyze framework performance
    var performance_metrics = cognitive_framework.analyze_framework_performance()
    
    # Optional: Print performance insights
    for metric_name, metric_value in performance_metrics:
        print("Performance Metric:", metric_name, "=", metric_value)
    
    return processed_input

fn main():
    # Example usage with different input types and complexities
    var numeric_data = [1.0, 2.0, 3.0, 4.0, 5.0]
    var processed_numeric = process_complex_data(numeric_data, 0.7)
    
    var text_data = ["cognitive", "adaptive", "framework"]
    var processed_text = process_complex_data(text_data, 0.5)
    
    # Reset framework for next cycle
    var cognitive_framework = IntelligentCognitiveFramework()
    cognitive_framework.reset_framework() 