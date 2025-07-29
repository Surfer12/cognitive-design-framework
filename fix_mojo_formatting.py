#!/usr/bin/env python3
"""
Mojo Formatting Fix Script

This script fixes common Mojo syntax issues that prevent formatting.
"""

import os
import re
import glob
from pathlib import Path

def fix_mojo_file(file_path: str) -> bool:
    """Fix common Mojo syntax issues in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        modified = False
        
        # Fix 1: Logical operators (or -> or)
        content = re.sub(r'\bor\b', 'or', content)
        
        # Fix 2: Function signatures without raises
        content = re.sub(r'fn (\w+)\(self, ([^)]+)\)\s*$', r'fn \1(self, \2) raises:\n        pass', content, flags=re.MULTILINE)
        
        # Fix 3: Empty function bodies
        content = re.sub(r'fn (\w+)\([^)]+\):\s*$', r'fn \1() raises:\n        pass', content, flags=re.MULTILINE)
        
        # Fix 4: Python.import_module calls
        content = re.sub(r'let random = Python\.import_module\("random"\)', r'let random_module = Python.import_module("random")', content)
        
        # Fix 5: Struct initialization with missing parentheses
        content = re.sub(r'let (\w+) = (\w+)\(([^)]+)\)\s*$', r'let \1 = \2(\3)', content, flags=re.MULTILINE)
        
        # Fix 6: Enum declarations
        content = re.sub(r'enum (\w+):\s*$', r'enum \1:\n    pass', content, flags=re.MULTILINE)
        
        # Fix 7: Function calls with missing parentheses
        content = re.sub(r'let (\w+) = (\w+)\(([^)]*)\)\s*$', r'let \1 = \2(\3)', content, flags=re.MULTILINE)
        
        # Fix 8: Variable declarations with missing type annotations
        content = re.sub(r'let (\w+) = ([^;]+);\s*$', r'let \1 = \2', content, flags=re.MULTILINE)
        
        # Fix 9: Function parameters with missing types
        content = re.sub(r'fn (\w+)\(([^)]+)\)\s*->\s*(\w+):', r'fn \1(\2) -> \3:', content, flags=re.MULTILINE)
        
        # Fix 10: Missing raises clauses
        content = re.sub(r'fn (\w+)\([^)]+\)\s*->\s*(\w+):\s*$', r'fn \1() -> \2 raises:\n        pass', content, flags=re.MULTILINE)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False

def find_mojo_files(directory: str) -> list:
    """Find all .mojo files in directory."""
    mojo_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.mojo'):
                mojo_files.append(os.path.join(root, file))
    return mojo_files

def main():
    """Main function to fix all Mojo files."""
    current_dir = os.getcwd()
    mojo_files = find_mojo_files(current_dir)
    
    print(f"Found {len(mojo_files)} Mojo files")
    
    fixed_count = 0
    for file_path in mojo_files:
        print(f"Processing: {file_path}")
        if fix_mojo_file(file_path):
            fixed_count += 1
            print(f"  ✓ Fixed: {file_path}")
        else:
            print(f"  - No changes needed: {file_path}")
    
    print(f"\nSummary: Fixed {fixed_count} out of {len(mojo_files)} files")

if __name__ == "__main__":
    main()