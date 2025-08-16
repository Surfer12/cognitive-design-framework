#!/usr/bin/env python3
"""
Fix import statement and pass statement issues introduced by previous refactoring.
"""

import os
import re
from pathlib import Path

def fix_import_and_pass_issues(filepath):
    """Fix import statements and pass statements that got corrupted."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix 1: Remove "= 0" from import statements
        content = re.sub(r'(from .+ import .+) = 0', r'\1', content)
        content = re.sub(r'(import .+) = 0', r'\1', content)
        
        # Fix 2: Remove "= 0" from pass statements
        content = re.sub(r'(\s+)pass = 0', r'\1pass', content)
        
        # Fix 3: Fix enum definitions that got corrupted
        content = re.sub(r'(enum \w+:)\s*pass = 0', r'\1\n    NONE = 0', content)
        
        # Fix 4: Fix struct definitions
        content = re.sub(r'struct (\w+):\s*$', r'struct \1:\n    pass', content, flags=re.MULTILINE)
        
        # Fix 5: Fix function signatures that got corrupted
        content = re.sub(r'(fn \w+\([^)]*\)[^:]*):$', r'\1:\n        pass', content, flags=re.MULTILINE)
        
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
    """Fix all Mojo files with import/pass issues."""
    project_root = Path("/Users/ryan_david_oates/cognitive-design-framework")
    
    # Find all .mojo files
    mojo_files = list(project_root.rglob("*.mojo"))
    
    print(f"Found {len(mojo_files)} Mojo files to fix...")
    
    fixed_count = 0
    for filepath in mojo_files:
        if fix_import_and_pass_issues(filepath):
            print(f"Fixed: {filepath}")
            fixed_count += 1
    
    print(f"\nFixed {fixed_count} files.")
    print("Run 'pixi run format' to test the improvements.")

if __name__ == "__main__":
    main()
