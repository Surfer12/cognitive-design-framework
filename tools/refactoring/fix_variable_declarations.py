#!/usr/bin/env python3
"""
Fix variable declaration and struct definition issues.
"""

import os
import re
from pathlib import Path

def fix_variable_declarations(filepath):
    """Fix variable declaration and struct issues."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix 1: Fix variable declarations with alias types
        content = re.sub(r'var (\w+): alias (\w+) = ""', r'var \1: \2', content)
        content = re.sub(r'var (\w+): alias (\w+) = ""', r'var \1: \2', content)
        
        # Fix 2: Fix struct definitions with inline variable declarations
        content = re.sub(
            r'struct (\w+):var (\w+): alias (\w+) = ""',
            r'struct \1:\n    var \2: \3',
            content
        )
        
        # Fix 3: Fix function definitions with missing colons and docstrings
        content = re.sub(
            r'fn (\w+)\([^)]*\):"""([^"]+)"""',
            r'fn \1(inout self):\n    """\2"""\n    pass',
            content
        )
        
        # Fix 4: Fix variable declarations at wrong indentation
        lines = content.split('\n')
        fixed_lines = []
        
        for i, line in enumerate(lines):
            if not line.strip():
                fixed_lines.append(line)
                continue
            
            # Fix variable declarations that should be inside structs
            if line.strip().startswith('var ') and not line.startswith('    '):
                # Check if we're inside a struct
                if i > 0:
                    prev_lines = lines[max(0, i-5):i]
                    in_struct = any('struct ' in prev_line for prev_line in prev_lines)
                    if in_struct:
                        line = '    ' + line.strip()
            
            # Fix function calls that should be inside functions
            if (line.strip().startswith(('self.', 'print(', 'return ')) and 
                not line.startswith('    ') and not line.startswith('        ')):
                line = '    ' + line.strip()
            
            fixed_lines.append(line)
        
        content = '\n'.join(fixed_lines)
        
        # Fix 5: Fix enum syntax
        content = re.sub(r'enum (\w+):\s*$', r'enum \1:\n    NONE = 0', content, flags=re.MULTILINE)
        
        # Fix 6: Fix trait syntax
        content = re.sub(r'trait (\w+):\s*$', r'trait \1:\n    pass', content, flags=re.MULTILINE)
        
        # Fix 7: Clean up malformed lines
        content = re.sub(r'<line number missing in source>', '', content)
        
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
    """Fix variable declaration issues in all Mojo files."""
    project_root = Path("/Users/ryan_david_oates/cognitive-design-framework")
    
    # Focus on files that are most likely to be fixed
    priority_files = [
        "basic_cognitive_demo.mojo",
        "cognitive_demo.mojo",
        "minimal_cognitive_demo.mojo",
        "working_cognitive_demo.mojo",
        "simple_cognitive_demo.mojo",
        "core/base/tag_element.mojo",
        "core/base/visitor.mojo",
        "src/core/tag_element.mojo",
        "src/core/visitor.mojo",
        "examples/core/tag_element.mojo",
        "examples/core/visitor.mojo",
        "examples/core/cognitive_tag_element.mojo"
    ]
    
    fixed_count = 0
    
    # Fix priority files first
    for filename in priority_files:
        filepath = project_root / filename
        if filepath.exists():
            if fix_variable_declarations(filepath):
                print(f"Fixed: {filepath}")
                fixed_count += 1
    
    # Fix other problematic files
    for filepath in project_root.rglob("*.mojo"):
        if filepath.name not in [f.split('/')[-1] for f in priority_files]:
            if fix_variable_declarations(filepath):
                print(f"Fixed: {filepath}")
                fixed_count += 1
    
    print(f"\nFixed {fixed_count} files with variable declaration issues.")
    print("Run 'pixi run format' to test the improvements.")

if __name__ == "__main__":
    main()
