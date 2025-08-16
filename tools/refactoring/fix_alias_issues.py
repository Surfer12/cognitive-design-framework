#!/usr/bin/env python3
"""
Fix alias and import statement issues.
"""

import os
import re
from pathlib import Path

def fix_alias_and_import_issues(filepath):
    """Fix alias and import statement problems."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix 1: Remove "alias" from import statements
        content = re.sub(r'(from .+ import .+) alias (.+) = 0', r'\1 \2', content)
        content = re.sub(r'(import .+) alias (.+) = 0', r'\1 \2', content)
        content = re.sub(r'from (.+) import alias (.+) = 0', r'from \1 import \2', content)
        
        # Fix 2: Remove "alias pass = 0" statements
        content = re.sub(r'\s*alias pass = 0\s*', '', content)
        
        # Fix 3: Fix standalone alias statements
        content = re.sub(r'alias (\w+) = 0', r'alias \1 = ""', content)
        
        # Fix 4: Clean up malformed lines
        lines = content.split('\n')
        fixed_lines = []
        
        for line in lines:
            # Skip empty or malformed lines
            if not line.strip():
                fixed_lines.append(line)
                continue
            
            # Fix import statements
            if 'import' in line and 'alias' in line:
                # Clean up import statements
                line = re.sub(r'alias (\w+)', r'\1', line)
                line = re.sub(r' = 0$', '', line)
            
            # Skip malformed alias lines
            if line.strip().startswith('alias') and '= 0' in line and 'pass' in line:
                continue
            
            fixed_lines.append(line)
        
        content = '\n'.join(fixed_lines)
        
        # Fix 5: Ensure proper function structure
        content = re.sub(r'fn (\w+)\(inout self\):\s*$', r'fn \1(inout self):\n    pass', content, flags=re.MULTILINE)
        
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
    """Fix alias issues in all Mojo files."""
    project_root = Path("/Users/ryan_david_oates/cognitive-design-framework")
    
    # Find all .mojo files
    mojo_files = list(project_root.rglob("*.mojo"))
    
    print(f"Found {len(mojo_files)} Mojo files to fix...")
    
    fixed_count = 0
    for filepath in mojo_files:
        if fix_alias_and_import_issues(filepath):
            print(f"Fixed: {filepath}")
            fixed_count += 1
    
    print(f"\nFixed {fixed_count} files.")
    print("Run 'pixi run format' to test the improvements.")

if __name__ == "__main__":
    main()
