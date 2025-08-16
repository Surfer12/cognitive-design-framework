#!/usr/bin/env python3
"""Fix common Mojo syntax errors that prevent formatting."""

import os
import re
from pathlib import Path

def fix_mojo_file(filepath):
    """Fix common syntax errors in a Mojo file."""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        original_content = content
        
        # Fix common patterns
        content = re.sub(r'from python import alias (\w+) = 0', r'from python import \1', content)
        content = re.sub(r'alias pass = 0', '', content)
        content = re.sub(r'^\s*pass\s*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'let (\w+) = ([^-\n]+) - ([^\n]+)', r'var \1 = \2 - \3', content)
        content = re.sub(r'from \.(\w+) import alias (\w+) = 0', r'from .\1 import \2', content)
        content = re.sub(r'from (\w+) import alias (\w+) = 0', r'from \1 import \2', content)
        
        # Remove empty lines created by removing pass statements
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        if content != original_content:
            with open(filepath, 'w') as f:
                f.write(content)
            print(f"Fixed: {filepath}")
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    """Fix all .mojo files in the project."""
    project_root = Path(__file__).parent
    fixed_count = 0
    
    for mojo_file in project_root.rglob("*.mojo"):
        if fix_mojo_file(mojo_file):
            fixed_count += 1
    
    print(f"Fixed {fixed_count} files")

if __name__ == "__main__":
    main()