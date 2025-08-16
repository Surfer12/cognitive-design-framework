# iXcan Pipeline Demonstration
# Comprehensive demo showing integration with cognitive framework

from ixcan_pipeline import (
    IXcanPipeline,
    CognitiveIXcanBridge,
    IXcanStage,
    CognitiveAnalysisProcessor,
    PatternRecognitionProcessor,
    AdaptiveOptimizationProcessor,
    IXcanContext,
    IXcanResult,
    demonstrate_ixcan_pipeline,
    demonstrate_cognitive_ixcan_bridge,
)

from examples import (
    TagInstance,
    TagAttribute,
    get_current_timestamp,
)

struct AdvancedCognitiveProcessor(IXcanProcessor):
    """Advanced processor demonstrating complex cognitive analysis."""
    var depth_analysis: Bool
    var meta_cognitive_awareness: Bool
    var adaptive_learning: Bool
    
    fn __init__(inout self):
        self.depth_analysis = True
        self.meta_cognitive_awareness = True
        self.adaptive_learning = True
    
    fn process(inout self, inout context: IXcanContext) raises -> IXcanResult:
        context.add_processing_step("advanced_cognitive_analysis")
        
        # Perform deep cognitive analysis
        let cognitive_depth = self.analyze_cognitive_depth(context.data)
        let meta_awareness = self.assess_meta_awareness(context)
        let learning_potential = self.evaluate_learning_potential(context)
        
        # Update cognitive state with advanced metrics
        context.cognitive_state.confidence_level = (cognitive_depth + meta_awareness + learning_potential) / 3.0
        
        var result = IXcanResult(True, context.data)
        result.set_metric("cognitive_depth", cognitive_depth)
        result.set_metric("meta_awareness", meta_awareness)
        result.set_metric("learning_potential", learning_potential)
        
        # Generate insights based on analysis
        if cognitive_depth > 0.8:
            result.add_insight("High cognitive depth detected - complex reasoning patterns identified")
        if meta_awareness > 0.7:
            result.add_insight("Strong meta-cognitive awareness - self-reflective processing active")
        if learning_potential > 0.6:
            result.add_insight("Significant learning potential - adaptive mechanisms engaged")
        
        # Generate recommendations
        if cognitive_depth < 0.5:
            result.add_recommendation("Consider increasing analysis depth for better understanding")
        if meta_awareness < 0.4:
            result.add_recommendation("Enable meta-cognitive reflection for enhanced processing")
        if learning_potential > 0.8:
            result.add_recommendation("High learning potential - consider advanced adaptation strategies")
        
        return result
    
    fn analyze_cognitive_depth(self, data: TagInstance) -> Float64:
        """Analyze the cognitive depth of the input data."""
        var depth_score = 0.0
        
        # Analyze attribute complexity
        for attribute in data.attributes:
            if len(attribute.value) > 50:
                depth_score += 0.2
            if attribute.value.find("complex") != -1:
                depth_score += 0.1
            if attribute.value.find("recursive") != -1:
                depth_score += 0.15
        
        # Analyze structural complexity
        if len(data.children) > 3:
            depth_score += 0.3
        
        return min(1.0, depth_score)
    
    fn assess_meta_awareness(self, context: IXcanContext) -> Float64:
        """Assess meta-cognitive awareness level."""
        var awareness_score = 0.5  # Base awareness
        
        # Check processing history for meta-cognitive indicators
        for step in context.processing_history:
            if step.find("meta") != -1:
                awareness_score += 0.1
            if step.find("reflection") != -1:
                awareness_score += 0.1
        
        # Factor in current cognitive state
        awareness_score += context.cognitive_state.attention_level * 0.2
        
        return min(1.0, awareness_score)
    
    fn evaluate_learning_potential(self, context: IXcanContext) -> Float64:
        """Evaluate the learning potential of the current context."""
        var learning_score = context.cognitive_state.adaptation_factor
        
        # Check for learning indicators in metadata
        if context.get_metadata("learning_enabled") == "true":
            learning_score += 0.3
        if context.get_metadata("adaptive_mode") == "active":
            learning_score += 0.2
        
        # Factor in complexity - higher complexity = higher learning potential
        learning_score += context.cognitive_state.complexity_score * 0.3
        
        return min(1.0, learning_score)

struct EmotionalIntelligenceProcessor(IXcanProcessor):
    """Processor for emotional intelligence analysis."""
    var emotion_detection: Bool
    var sentiment_analysis: Bool
    var empathy_modeling: Bool
    
    fn __init__(inout self):
        self.emotion_detection = True
        self.sentiment_analysis = True
        self.empathy_modeling = True
    
    fn process(inout self, inout context: IXcanContext) raises -> IXcanResult:
        context.add_processing_step("emotional_intelligence_analysis")
        
        let emotional_valence = self.detect_emotional_valence(context.data)
        let sentiment_score = self.analyze_sentiment(context.data)
        let empathy_level = self.model_empathy(context)
        
        var result = IXcanResult(True, context.data)
        result.set_metric("emotional_valence", emotional_valence)
        result.set_metric("sentiment_score", sentiment_score)
        result.set_metric("empathy_level", empathy_level)
        
        # Generate emotional insights
        if emotional_valence > 0.6:
            result.add_insight("Positive emotional context detected")
        elif emotional_valence < 0.4:
            result.add_insight("Negative emotional context detected")
        else:
            result.add_insight("Neutral emotional context")
        
        if sentiment_score > 0.7:
            result.add_insight("Highly positive sentiment")
        elif sentiment_score < 0.3:
            result.add_insight("Negative sentiment detected")
        
        if empathy_level > 0.8:
            result.add_recommendation("High empathy context - consider emotional support strategies")
        
        return result
    
    fn detect_emotional_valence(self, data: TagInstance) -> Float64:
        """Detect emotional valence in the data."""
        var valence = 0.5  # Neutral baseline
        
        for attribute in data.attributes:
            let value = attribute.value.lower()
            if value.find("happy") != -1 or value.find("joy") != -1:
                valence += 0.2
            elif value.find("sad") != -1 or value.find("angry") != -1:
                valence -= 0.2
            elif value.find("excited") != -1 or value.find("positive") != -1:
                valence += 0.15
            elif value.find("negative") != -1 or value.find("frustrated") != -1:
                valence -= 0.15
        
        return max(0.0, min(1.0, valence))
    
    fn analyze_sentiment(self, data: TagInstance) -> Float64:
        """Analyze sentiment polarity."""
        var sentiment = 0.5  # Neutral baseline
        
        # Simple sentiment analysis based on keywords
        for attribute in data.attributes:
            let value = attribute.value.lower()
            if value.find("good") != -1 or value.find("great") != -1:
                sentiment += 0.1
            elif value.find("bad") != -1 or value.find("terrible") != -1:
                sentiment -= 0.1
            elif value.find("excellent") != -1 or value.find("amazing") != -1:
                sentiment += 0.2
            elif value.find("awful") != -1 or value.find("horrible") != -1:
                sentiment -= 0.2
        
        return max(0.0, min(1.0, sentiment))
    
    fn model_empathy(self, context: IXcanContext) -> Float64:
        """Model empathy level based on context."""
        var empathy = 0.5  # Base empathy level
        
        # Higher empathy for emotional content
        let emotional_indicators = context.get_metadata("emotional_content")
        if emotional_indicators == "high":
            empathy += 0.3
        elif emotional_indicators == "medium":
            empathy += 0.1
        
        # Adjust based on cognitive state
        empathy += context.cognitive_state.attention_level * 0.2
        
        return min(1.0, empathy)

struct ComprehensiveIXcanDemo:
    """Comprehensive demonstration of iXcan pipeline capabilities."""
    var pipeline: IXcanPipeline
    var bridge: CognitiveIXcanBridge
    
    fn __init__(inout self):
        self.pipeline = IXcanPipeline()
        self.bridge = CognitiveIXcanBridge()
        self.setup_advanced_pipeline()
    
    fn setup_advanced_pipeline(inout self):
        """Setup pipeline with advanced processors."""
        # Add advanced cognitive processor
        let advanced_processor = AdvancedCognitiveProcessor()
        let advanced_stage = IXcanStage("advanced_cognitive", advanced_processor)
        self.pipeline.add_stage(advanced_stage)
        
        # Add emotional intelligence processor
        let emotional_processor = EmotionalIntelligenceProcessor()
        let emotional_stage = IXcanStage("emotional_intelligence", emotional_processor)
        self.pipeline.add_stage(emotional_stage)
    
    fn run_comprehensive_demo(inout self) raises:
        """Run comprehensive demonstration of all capabilities."""
        print("=== Comprehensive iXcan Pipeline Demo ===\n")
        
        # Demo 1: Basic cognitive analysis
        print("1. Basic Cognitive Analysis:")
        self.demo_basic_cognitive_analysis()
        
        # Demo 2: Complex pattern recognition
        print("\n2. Complex Pattern Recognition:")
        self.demo_complex_pattern_recognition()
        
        # Demo 3: Emotional intelligence processing
        print("\n3. Emotional Intelligence Processing:")
        self.demo_emotional_intelligence()
        
        # Demo 4: Adaptive optimization
        print("\n4. Adaptive Optimization:")
        self.demo_adaptive_optimization()
        
        # Demo 5: Full pipeline integration
        print("\n5. Full Pipeline Integration:")
        self.demo_full_integration()
        
        # Demo 6: Performance metrics
        print("\n6. Performance Metrics:")
        self.demo_performance_metrics()
    
    fn demo_basic_cognitive_analysis(inout self) raises:
        """Demonstrate basic cognitive analysis."""
        var test_tag = TagInstance(
            name="cognitive_test",
            attributes=[
                TagAttribute("content", "Analyze this cognitive pattern with recursive elements"),
                TagAttribute("complexity", "medium"),
                TagAttribute("type", "analytical_thinking")
            ],
            children=[]
        )
        
        let result = self.pipeline.process(test_tag)
        self.print_result_summary(result, "Basic Cognitive Analysis")
    
    fn demo_complex_pattern_recognition(inout self) raises:
        """Demonstrate complex pattern recognition."""
        var complex_tag = TagInstance(
            name="pattern_analysis",
            attributes=[
                TagAttribute("content", "Complex recursive feedback adaptive behavior patterns"),
                TagAttribute("structure", "hierarchical_organization"),
                TagAttribute("behavior", "adaptive_learning")
            ],
            children=[
                TagInstance("child1", [], []),
                TagInstance("child2", [], []),
                TagInstance("child3", [], [])
            ]
        )
        
        let result = self.pipeline.process(complex_tag)
        self.print_result_summary(result, "Complex Pattern Recognition")
    
    fn demo_emotional_intelligence(inout self) raises:
        """Demonstrate emotional intelligence processing."""
        var emotional_tag = TagInstance(
            name="emotional_content",
            attributes=[
                TagAttribute("content", "I feel excited and happy about this amazing discovery"),
                TagAttribute("emotion", "positive"),
                TagAttribute("sentiment", "excellent")
            ],
            children=[]
        )
        
        let result = self.pipeline.process(emotional_tag)
        self.print_result_summary(result, "Emotional Intelligence")
    
    fn demo_adaptive_optimization(inout self) raises:
        """Demonstrate adaptive optimization."""
        var optimization_tag = TagInstance(
            name="optimization_test",
            attributes=[
                TagAttribute("content", "Optimize this complex cognitive process"),
                TagAttribute("complexity", "high"),
                TagAttribute("optimization_target", "performance")
            ],
            children=[]
        )
        
        # Set metadata for learning
        var context = IXcanContext(optimization_tag)
        context.set_metadata("learning_enabled", "true")
        context.set_metadata("adaptive_mode", "active")
        
        let result = self.pipeline.process(optimization_tag)
        self.print_result_summary(result, "Adaptive Optimization")
    
    fn demo_full_integration(inout self) raises:
        """Demonstrate full pipeline integration with cognitive bridge."""
        let input = "Please analyze this complex emotional and cognitive pattern with recursive feedback loops and provide adaptive optimization recommendations"
        
        let response = self.bridge.process_cognitive_input(input)
        print("Integrated Response: " + response)
        
        let analysis = self.bridge.get_comprehensive_analysis(input)
        print("\nComprehensive Analysis:")
        print(analysis)
    
    fn demo_performance_metrics(inout self):
        """Demonstrate performance metrics."""
        print("Pipeline Performance Metrics:")
        print(self.pipeline.get_pipeline_status())
        
        print("\nStage-by-Stage Metrics:")
        for i in range(len(self.pipeline.stages)):
            let stage = self.pipeline.stages[i]
            print("Stage: " + stage.name)
            print("  Executions: " + str(stage.metrics.execution_count))
            print("  Success Rate: " + str(Float64(stage.metrics.success_count) / Float64(stage.metrics.execution_count) * 100.0) + "%")
            print("  Avg Execution Time: " + str(stage.metrics.average_execution_time) + "ms")
    
    fn print_result_summary(self, result: IXcanResult, demo_name: String):
        """Print a summary of processing results."""
        print("Demo: " + demo_name)
        print("Success: " + str(result.success))
        print("Key Insights:")
        for insight in result.insights[0:min(3, len(result.insights))]:  # Show first 3 insights
            print("  • " + insight)
        print("Key Recommendations:")
        for rec in result.recommendations[0:min(2, len(result.recommendations))]:  # Show first 2 recommendations
            print("  → " + rec)
        print("Metrics Count: " + str(len(result.metrics)))

fn run_interactive_demo():
    """Run an interactive demo session."""
    print("=== Interactive iXcan Pipeline Demo ===")
    print("This demo showcases the Interactive eXtensible Cognitive ANalysis pipeline")
    print("built on your existing cognitive design framework.\n")
    
    var demo = ComprehensiveIXcanDemo()
    
    try:
        demo.run_comprehensive_demo()
        
        print("\n" + "="*60)
        print("iXcan Pipeline Features Demonstrated:")
        print("✓ Cognitive complexity analysis")
        print("✓ Pattern recognition and classification")
        print("✓ Emotional intelligence processing")
        print("✓ Adaptive optimization strategies")
        print("✓ Meta-cognitive awareness assessment")
        print("✓ Integration with existing cognitive bridge")
        print("✓ Comprehensive performance metrics")
        print("✓ Extensible stage-based architecture")
        print("="*60)
        
    except e:
        print("Demo error: " + str(e))

fn main():
    """Main function to run all demonstrations."""
    print("Starting iXcan Pipeline Comprehensive Demonstration\n")
    
    # Run basic demos
    demonstrate_ixcan_pipeline()
    demonstrate_cognitive_ixcan_bridge()
    
    # Run interactive comprehensive demo
    print("\n" + "="*60)
    run_interactive_demo()
    
    print("\niXcan Pipeline demonstration completed successfully!")
    print("The pipeline is ready for integration with your cognitive design framework.")
