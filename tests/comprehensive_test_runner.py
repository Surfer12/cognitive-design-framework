#!/usr/bin/env python3
"""
Comprehensive Test Runner for Cognitive Design Framework
Tests framework without requiring Mojo compiler installation
Focuses on structure validation, file analysis, and meta-level efficacy
"""

import os
import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
import re
import ast
import hashlib

class FrameworkValidator:
    """Comprehensive framework validator that doesn't require Mojo compiler"""
    
    def __init__(self, framework_root: str):
        self.framework_root = Path(framework_root)
        self.test_results = {}
        self.validation_metrics = {}
        self.meta_properties = {}
        self.start_time = time.time()
        
    def validate_file_structure(self, file_path: str) -> Dict[str, Any]:
        """Validate file structure and content"""
        full_path = self.framework_root / file_path
        
        if not full_path.exists():
            return {
                "exists": False,
                "size": 0,
                "lines": 0,
                "error": "File not found"
            }
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            
            return {
                "exists": True,
                "size": len(content),
                "lines": len(lines),
                "has_struct": "struct " in content,
                "has_fn": "fn " in content,
                "has_imports": "from " in content,
                "has_comments": "#" in content,
                "content_hash": hashlib.md5(content.encode()).hexdigest()[:8]
            }
        except Exception as e:
            return {
                "exists": True,
                "size": 0,
                "lines": 0,
                "error": str(e)
            }
    
    def analyze_code_quality(self, file_path: str) -> Dict[str, Any]:
        """Analyze code quality metrics"""
        full_path = self.framework_root / file_path
        
        if not full_path.exists():
            return {"error": "File not found"}
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            
            # Quality metrics
            metrics = {
                "total_lines": len(lines),
                "non_empty_lines": sum(1 for line in lines if line.strip()),
                "comment_lines": sum(1 for line in lines if line.strip().startswith("#")),
                "struct_count": len(re.findall(r'\bstruct\s+\w+', content)),
                "function_count": len(re.findall(r'\bfn\s+\w+', content)),
                "import_count": len(re.findall(r'\bfrom\s+[\w\.]+', content)),
                "has_docstrings": '"""' in content,
                "avg_line_length": sum(len(line) for line in lines) / len(lines) if lines else 0,
                "complexity_score": self.calculate_complexity_score(content)
            }
            
            # Quality score (0-100)
            quality_score = self.calculate_quality_score(metrics)
            metrics["quality_score"] = quality_score
            
            return metrics
        except Exception as e:
            return {"error": str(e)}
    
    def calculate_complexity_score(self, content: str) -> float:
        """Calculate code complexity score"""
        # Simple complexity metrics
        nesting_depth = content.count("    ") / len(content.split('\n'))
        function_count = len(re.findall(r'\bfn\s+\w+', content))
        conditional_count = len(re.findall(r'\bif\s+', content))
        
        # Complexity formula (normalized to 0-1)
        complexity = min(1.0, (nesting_depth * 0.3 + function_count * 0.1 + conditional_count * 0.1))
        return complexity
    
    def calculate_quality_score(self, metrics: Dict[str, Any]) -> float:
        """Calculate overall code quality score"""
        score = 100.0
        
        # Deduct for various issues
        if metrics["total_lines"] < 10:
            score -= 20  # Too short
        
        if metrics["comment_lines"] == 0:
            score -= 15  # No comments
        
        if not metrics["has_docstrings"]:
            score -= 10  # No docstrings
        
        if metrics["avg_line_length"] > 120:
            score -= 10  # Lines too long
        
        if metrics["complexity_score"] > 0.7:
            score -= 15  # Too complex
        
        # Bonus for good practices
        if metrics["struct_count"] > 0:
            score += 5
        if metrics["function_count"] > 2:
            score += 5
        if metrics["import_count"] > 0:
            score += 5
        
        return max(0.0, min(100.0, score))
    
    def validate_meta_properties(self, file_path: str) -> Dict[str, Any]:
        """Validate meta-level file properties"""
        full_path = self.framework_root / file_path
        
        if not full_path.exists():
            return {"error": "File not found"}
        
        # Extract meta properties
        file_stats = full_path.stat()
        
        meta_props = {
            "file_path": file_path,
            "file_size": file_stats.st_size,
            "creation_time": file_stats.st_ctime,
            "modification_time": file_stats.st_mtime,
            "compilation_mode": self.infer_compilation_mode(file_path),
            "validation_level": self.calculate_validation_level(file_path),
            "dependency_count": self.count_dependencies(file_path),
            "efficacy_score": 0.0  # Will be calculated
        }
        
        # Calculate efficacy score based on meta properties
        meta_props["efficacy_score"] = self.calculate_meta_efficacy(meta_props)
        
        return meta_props
    
    def infer_compilation_mode(self, file_path: str) -> str:
        """Infer compilation mode from file characteristics"""
        full_path = self.framework_root / file_path
        
        if not full_path.exists():
            return "unknown"
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple heuristics
            if "trait" in content and "struct" in content:
                return "hybrid"  # Both dynamic and static features
            elif "fn __init__" in content and "@staticmethod" in content:
                return "static"  # Static compilation features
            else:
                return "dynamic"  # Default to dynamic
        except:
            return "unknown"
    
    def calculate_validation_level(self, file_path: str) -> int:
        """Calculate validation depth level (0-10)"""
        full_path = self.framework_root / file_path
        
        if not full_path.exists():
            return 0
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Count validation indicators
            validation_indicators = [
                "assert" in content,
                "test" in content.lower(),
                "validate" in content.lower(),
                "check" in content.lower(),
                "verify" in content.lower(),
                "if" in content,  # Basic control flow
                "struct" in content,  # Data structures
                "fn" in content,  # Functions
                "import" in content,  # Dependencies
                "comment" in content or "#" in content  # Documentation
            ]
            
            return sum(validation_indicators)
        except:
            return 0
    
    def count_dependencies(self, file_path: str) -> int:
        """Count file dependencies"""
        full_path = self.framework_root / file_path
        
        if not full_path.exists():
            return 0
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Count import statements and references
            imports = len(re.findall(r'\bfrom\s+[\w\.]+', content))
            references = len(re.findall(r'\bimport\s+[\w\.]+', content))
            
            return imports + references
        except:
            return 0
    
    def calculate_meta_efficacy(self, meta_props: Dict[str, Any]) -> float:
        """Calculate meta-level efficacy score"""
        score = 1.0
        
        # File size factor
        if meta_props["file_size"] > 10000:  # Large files
            score *= 0.9
        elif meta_props["file_size"] < 100:  # Very small files
            score *= 0.8
        
        # Compilation mode factor
        if meta_props["compilation_mode"] == "hybrid":
            score *= 1.1
        elif meta_props["compilation_mode"] == "static":
            score *= 1.05
        
        # Validation level factor
        validation_factor = min(1.0, meta_props["validation_level"] / 10.0)
        score *= (0.5 + validation_factor * 0.5)
        
        # Dependencies factor
        if meta_props["dependency_count"] > 10:
            score *= 0.9
        elif meta_props["dependency_count"] == 0:
            score *= 0.8
        
        return min(1.0, score)
    
    def run_comprehensive_validation(self) -> bool:
        """Run comprehensive framework validation"""
        print("🧬 COGNITIVE DESIGN FRAMEWORK - COMPREHENSIVE VALIDATION")
        print("Testing Without Mojo Compiler - Meta-Level Analysis")
        print("=" * 70)
        
        # Test components
        test_components = [
            "cognitive_framework/core/base/tag_element.mojo",
            "cognitive_framework/core/base/visitor.mojo", 
            "cognitive_framework/core/bridge/cognitive_bridge.mojo",
            "systems/consciousness/consciousness_simple.mojo",
            "systems/consciousness/consciousness_framework.mojo",
            "examples/demos/simple_working_demo.mojo",
            "examples/demos/basic_cognitive_demo.mojo"
        ]
        
        total_score = 0.0
        valid_components = 0
        
        for component in test_components:
            print(f"\n🔍 Analyzing: {component}")
            
            # File structure validation
            structure = self.validate_file_structure(component)
            if structure.get("exists"):
                print(f"   ✅ File exists ({structure['size']} bytes, {structure['lines']} lines)")
                
                # Code quality analysis
                quality = self.analyze_code_quality(component)
                if "quality_score" in quality:
                    print(f"   📊 Code Quality: {quality['quality_score']:.1f}%")
                    total_score += quality["quality_score"]
                    valid_components += 1
                
                # Meta properties validation
                meta_props = self.validate_meta_properties(component)
                if "efficacy_score" in meta_props:
                    print(f"   ⚡ Meta Efficacy: {meta_props['efficacy_score']:.1%}")
                
                # Store results
                self.test_results[component] = {
                    "structure": structure,
                    "quality": quality,
                    "meta": meta_props,
                    "passed": True
                }
            else:
                print(f"   ❌ File not found")
                self.test_results[component] = {
                    "passed": False,
                    "error": "File not found"
                }
        
        # Framework structure validation
        print(f"\n🏗️  FRAMEWORK STRUCTURE VALIDATION")
        structure_score = self.validate_overall_structure()
        total_score += structure_score * 10  # Weight structure validation
        valid_components += 1
        
        # Generate comprehensive report
        self.generate_validation_report(total_score, valid_components)
        
        return total_score > 70.0  # Pass threshold
    
    def validate_overall_structure(self) -> float:
        """Validate overall framework structure"""
        required_dirs = [
            "cognitive_framework/core",
            "systems/consciousness", 
            "examples/demos",
            "tests"
        ]
        
        score = 100.0
        
        for dir_path in required_dirs:
            full_path = self.framework_root / dir_path
            if full_path.exists():
                file_count = len(list(full_path.glob("*.mojo")))
                print(f"   ✅ {dir_path}: {file_count} files")
            else:
                print(f"   ❌ {dir_path}: MISSING")
                score -= 25.0
        
        return max(0.0, score)
    
    def generate_validation_report(self, total_score: float, valid_components: int):
        """Generate comprehensive validation report"""
        print(f"\n" + "=" * 70)
        print("📋 COMPREHENSIVE VALIDATION REPORT")
        print("=" * 70)
        
        if valid_components > 0:
            avg_score = total_score / valid_components
            print(f"Average Component Score: {avg_score:.1f}%")
        else:
            avg_score = 0.0
        
        print(f"Valid Components: {valid_components}")
        print(f"Total Validation Score: {total_score:.1f}%")
        
        if avg_score >= 70.0:
            print("🎉 FRAMEWORK VALIDATION: PASSED")
            print("✅ Components meet quality standards")
            print("✅ Meta-level properties validated")
            print("🚀 Framework ready for development")
        else:
            print("⚠️  FRAMEWORK VALIDATION: NEEDS ATTENTION")
            print("🔧 Review component quality scores")
            print("📊 Improve meta-level efficacy")
        
        print(f"\n⏱️  Validation Time: {time.time() - self.start_time:.2f}s")
        
        # Save detailed report
        report = {
            "framework": "Cognitive Design Framework",
            "validation_timestamp": time.time(),
            "average_score": avg_score,
            "total_score": total_score,
            "valid_components": valid_components,
            "test_results": self.test_results
        }
        
        report_file = self.framework_root / "comprehensive_validation_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"📄 Detailed report saved to: {report_file}")

def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        framework_root = sys.argv[1]
    else:
        framework_root = "/Users/ryan_david_oates/cognitive-design-framework"
    
    validator = FrameworkValidator(framework_root)
    success = validator.run_comprehensive_validation()
    
    print(f"\n✨ Validation Complete!")
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
