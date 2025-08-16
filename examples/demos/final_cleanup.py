#!/usr/bin/env python3
"""
Final cleanup script for remaining critical Mojo syntax issues.
"""

import os
import re
from pathlib import Path

def final_cleanup(filepath):
    """Apply final cleanup fixes."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix 1: Remove "= 0" from various statements
        content = re.sub(r'(\s+.+) = 0$', r'\1', content, flags=re.MULTILINE)
        
        # Fix 2: Fix function parameter issues
        content = re.sub(r'inoutself', r'inout self', content)
        
        # Fix 3: Fix incomplete function signatures
        content = re.sub(r'fn (\w+)\(:$', r'fn \1(inout self):', content, flags=re.MULTILINE)
        
        # Fix 4: Fix enum syntax
        content = re.sub(r'(enum \w+:)\s*pass', r'\1\n    NONE = 0', content)
        
        # Fix 5: Fix incomplete generic function syntax
        content = re.sub(r'(\s+)\](\([^)]*\))', r'\1](inout self\2', content)
        
        # Fix 6: Fix return statements
        content = re.sub(r'return\s*$', r'return ""', content, flags=re.MULTILINE)
        
        # Fix 7: Fix indentation issues by normalizing whitespace
        lines = content.split('\n')
        fixed_lines = []
        
        for i, line in enumerate(lines):
            # Skip empty lines
            if not line.strip():
                fixed_lines.append(line)
                continue
            
            # Fix basic indentation consistency
            if line.strip() and not line.startswith('    ') and not line.startswith('struct') and not line.startswith('fn ') and not line.startswith('from ') and not line.startswith('import ') and not line.startswith('#'):
                # Check if this should be indented based on context
                if i > 0:
                    prev_line = lines[i-1].strip()
                    if prev_line.endswith(':') or 'fn ' in prev_line:
                        if not line.startswith('    '):
                            line = '    ' + line.strip()
            
            fixed_lines.append(line)
        
        content = '\n'.join(fixed_lines)
        
        # Fix 8: Clean up malformed syntax
        content = re.sub(r':\s*$', r':\n        pass', content, flags=re.MULTILINE)
        
        # Only write if content changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    """Apply final cleanup to all Mojo files."""
    project_root = Path("/Users/ryan_david_oates/cognitive-design-framework")
    
    # Focus on the most problematic files first
    priority_files = [
        "basic_cognitive_demo.mojo",
        "cognitive_demo.mojo",
        "cognitive_framework_demo.mojo", 
        "demo.mojo",
        "minimal_cognitive_demo.mojo",
        "working_cognitive_demo.mojo",
        "simple_cognitive_demo.mojo"
    ]
    
    fixed_count = 0
    
    # Fix priority files first
    for filename in priority_files:
        filepath = project_root / filename
        if filepath.exists():
            if final_cleanup(filepath):
                print(f"Fixed: {filepath}")
                fixed_count += 1
    
    # Fix all other .mojo files
    for filepath in project_root.rglob("*.mojo"):
        if filepath.name not in priority_files:
            if final_cleanup(filepath):
                print(f"Fixed: {filepath}")
                fixed_count += 1
    
    print(f"\nFinal cleanup complete! Fixed {fixed_count} files.")
    print("Run 'pixi run format' to test the final results.")

if __name__ == "__main__":
    main()
