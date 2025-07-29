#!/usr/bin/env python3
"""
Fix indentation issues in Mojo files.
"""

import os
import re
from pathlib import Path

def fix_indentation(filepath):
    """Fix basic indentation issues."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Split into lines and fix indentation
        lines = content.split('\n')
        fixed_lines = []
        
        for i, line in enumerate(lines):
            # Skip empty lines
            if not line.strip():
                fixed_lines.append(line)
                continue
            
            # Don't modify top-level declarations
            if (line.startswith('from ') or 
                line.startswith('import ') or 
                line.startswith('struct ') or 
                line.startswith('fn ') or
                line.startswith('#') or
                line.startswith('"""')):
                fixed_lines.append(line)
                continue
            
            # Fix over-indented lines (more than 8 spaces)
            if line.startswith('        '):  # 8+ spaces
                # Keep reasonable indentation (4 spaces for function body)
                stripped = line.lstrip()
                if stripped:
                    line = '    ' + stripped
            
            fixed_lines.append(line)
        
        content = '\n'.join(fixed_lines)
        
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
    """Fix indentation in all Mojo files."""
    project_root = Path("/Users/ryan_david_oates/cognitive-design-framework")
    
    # Find all .mojo files
    mojo_files = list(project_root.rglob("*.mojo"))
    
    print(f"Found {len(mojo_files)} Mojo files to fix...")
    
    fixed_count = 0
    for filepath in mojo_files:
        if fix_indentation(filepath):
            print(f"Fixed: {filepath}")
            fixed_count += 1
    
    print(f"\nFixed indentation in {fixed_count} files.")
    print("Run 'pixi run format' to test the results.")

if __name__ == "__main__":
    main()
