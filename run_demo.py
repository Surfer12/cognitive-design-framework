#!/usr/bin/env python3
"""
Demo Script for Red Team Evaluation Framework

This script demonstrates the complete workflow of the red team evaluation
framework using the UPOF whitepaper vulnerability assessment.
"""

import json
import time
from datetime import datetime
from red_team_framework import RedTeamFramework, ModelConfig
from mathematical_validation import MathematicalValidator

def run_mathematical_validation_demo():
    """Run the mathematical validation demo."""
    
    print("=" * 60)
    print("MATHEMATICAL VALIDATION DEMO")
    print("=" * 60)
    
    validator = MathematicalValidator()
    results = validator.run_full_validation()
    
    print("\nMathematical Validation Results:")
    print("-" * 40)
    
    for theorem, result in results.items():
        if theorem == "summary":
            continue
            
        print(f"\n{theorem.replace('_', ' ').title()}:")
        if isinstance(result, dict):
            for key, value in result.items():
                if key != "is_incorrect":
                    print(f"  {key}: {value}")
            status = "❌ INCORRECT" if result.get('is_incorrect') else "✅ CORRECT"
            print(f"  Status: {status}")
    
    # Print summary
    summary = results["summary"]
    print(f"\nSummary:")
    print(f"  Total Claims Analyzed: {summary['total_claims_analyzed']}")
    print(f"  Incorrect Claims: {summary['incorrect_claims']}")
    print(f"  Error Rate: {summary['error_rate']:.1%}")
    print(f"  Validation Status: {summary['validation_status']}")

def run_red_team_assessment_demo():
    """Run the red team assessment demo."""
    
    print("\n" + "=" * 60)
    print("RED TEAM ASSESSMENT DEMO")
    print("=" * 60)
    
    # Initialize framework
    framework = RedTeamFramework()
    framework.load_test_cases()
    
    # Add demo models
    demo_models = [
        ModelConfig("Demo-GPT-4", "OpenAI", "api.openai.com/v1"),
        ModelConfig("Demo-Claude-3", "Anthropic", "api.anthropic.com"),
        ModelConfig("Demo-Gemini", "Google", "generativelanguage.googleapis.com")
    ]
    
    for model in demo_models:
        framework.add_model(model)
    
    print(f"\nLoaded {len(framework.test_cases)} test cases")
    print(f"Added {len(framework.models)} target models")
    
    # Run a small demo assessment
    print("\nRunning demo assessment (5 iterations per test)...")
    report = framework.run_full_assessment(iterations_per_test=5)
    
    # Display results
    print("\nAssessment Results:")
    print("-" * 40)
    
    summary = report["summary"]
    print(f"Total Tests: {summary['total_tests']}")
    print(f"Vulnerabilities Detected: {summary['vulnerabilities_detected']}")
    print(f"Detection Rate: {summary['detection_rate']:.1%}")
    print(f"False Positive Rate: {summary['false_positive_rate']:.1%}")
    print(f"Average Severity: {summary['average_severity']:.1f}/5")
    print(f"Average Breadth: {summary['average_breadth']:.1f}/5")
    
    # Show category breakdown
    print("\nCategory Breakdown:")
    for category, stats in report["category_breakdown"].items():
        rate = stats["vulnerabilities"] / stats["total"] if stats["total"] > 0 else 0
        print(f"  {category}: {stats['vulnerabilities']}/{stats['total']} ({rate:.1%})")
    
    # Show recommendations
    print("\nRecommendations:")
    for rec in report["recommendations"]:
        print(f"  - {rec}")
    
    return report

def demonstrate_test_cases():
    """Demonstrate individual test cases."""
    
    print("\n" + "=" * 60)
    print("TEST CASE DEMONSTRATION")
    print("=" * 60)
    
    framework = RedTeamFramework()
    framework.load_test_cases()
    
    # Show test case details
    for i, test_case in enumerate(framework.test_cases, 1):
        print(f"\n{i}. {test_case.name}")
        print(f"   Category: {test_case.category}")
        print(f"   Vulnerability Type: {test_case.vulnerability_type}")
        print(f"   Severity: {test_case.severity_score}/5")
        print(f"   Breadth: {test_case.breadth_score}/5")
        print(f"   Proof Basis: {test_case.proof_basis}")
        print(f"   Mathematical Error: {test_case.mathematical_error}")
        
        print("   Sample Prompts:")
        for j, prompt in enumerate(test_case.prompts[:2], 1):  # Show first 2 prompts
            print(f"     {j}. {prompt}")
        
        print(f"   Expected Desired: {test_case.expected_desired}")
        print(f"   Expected Undesired: {test_case.expected_undesired}")

def demonstrate_adversarial_prompts():
    """Demonstrate adversarial prompt generation."""
    
    print("\n" + "=" * 60)
    print("ADVERSARIAL PROMPT DEMONSTRATION")
    print("=" * 60)
    
    framework = RedTeamFramework()
    framework.load_test_cases()
    
    prompt_types = ["direct", "self_application", "historical"]
    
    for test_case in framework.test_cases[:3]:  # Show first 3 test cases
        print(f"\n{test_case.name}:")
        print(f"  Vulnerability Type: {test_case.vulnerability_type}")
        
        for prompt_type in prompt_types:
            prompt = framework.generate_adversarial_prompt(test_case, prompt_type)
            print(f"  {prompt_type.title()} Prompt: {prompt}")

def save_demo_results(report):
    """Save demo results to file."""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"demo_results_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nDemo results saved to: {filename}")

def main():
    """Run the complete demo."""
    
    print("Red Team Evaluation Framework - Demo")
    print("Testing AI Model Vulnerabilities Using UPOF Whitepaper")
    print("=" * 60)
    
    try:
        # Run mathematical validation
        run_mathematical_validation_demo()
        
        # Demonstrate test cases
        demonstrate_test_cases()
        
        # Demonstrate adversarial prompts
        demonstrate_adversarial_prompts()
        
        # Run red team assessment
        report = run_red_team_assessment_demo()
        
        # Save results
        save_demo_results(report)
        
        print("\n" + "=" * 60)
        print("DEMO COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print("\nThe framework has demonstrated:")
        print("✅ Mathematical validation of UPOF errors")
        print("✅ Test case generation and management")
        print("✅ Adversarial prompt creation")
        print("✅ Vulnerability detection and scoring")
        print("✅ Comprehensive reporting")
        print("✅ Ethical testing methodology")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        print("Please check that all dependencies are installed:")
        print("pip install -r requirements.txt")

if __name__ == "__main__":
    main()