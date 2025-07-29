#!/usr/bin/env python3
"""
Script to fix common Mojo syntax issues in the cognitive design framework.
"""

import os
import re
import glob

def fix_mojo_file(filepath):
    """Fix common syntax issues in a single Mojo file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix 1: Add missing return type and colon to __init__ methods
        content = re.sub(
            r'fn __init__\(inout self\)\s*$',
            r'fn __init__(inout self):',
            content,
            flags=re.MULTILINE
        )
        
        # Fix 2: Add missing return type to __init__ methods that raise
        content = re.sub(
            r'fn __init__\(\) -> None raises:\s*$',
            r'fn __init__(inout self) raises:',
            content,
            flags=re.MULTILINE
        )
        
        # Fix 3: Fix incomplete function signatures (missing colon)
        content = re.sub(
            r'fn (\w+)\([^)]*\)\s*$',
            lambda m: f"{m.group(0)}:" if not m.group(0).endswith(':') else m.group(0),
            content,
            flags=re.MULTILINE
        )
        
        # Fix 4: Fix visitor function signatures
        content = re.sub(
            r'fn visit_tag_element\(\)\s*$',
            r'fn visit_tag_element(inout self, element: TagElement):',
            content,
            flags=re.MULTILINE
        )
        
        # Fix 5: Fix accept method signatures
        content = re.sub(
            r'fn accept\(inout self, \)\s*$',
            r'fn accept(inout self, visitor: Visitor):',
            content,
            flags=re.MULTILINE
        )
        
        # Fix 6: Fix main function signatures
        content = re.sub(
            r'fn main\(\)\s*$',
            r'fn main():',
            content,
            flags=re.MULTILINE
        )
        
        # Fix 7: Fix enum declarations
        content = re.sub(
            r'enum (\w+):\s*$',
            r'enum \1:',
            content,
            flags=re.MULTILINE
        )
        
        # Fix 8: Fix let declarations (remove type annotations that cause issues)
        content = re.sub(
            r'let (\w+): String = ',
            r'alias \1 = ',
            content
        )
        
        # Fix 9: Fix function return type declarations
        content = re.sub(
            r'fn __init__\(inout self\) -> Self\s*$',
            r'fn __init__(inout self):',
            content,
            flags=re.MULTILINE
        )
        
        # Fix 10: Add missing colons to function definitions
        lines = content.split('\n')
        fixed_lines = []
        
        for line in lines:
            # Check if it's a function definition missing a colon
            if re.match(r'\s*fn \w+\([^)]*\)\s*$', line) and not line.endswith(':'):
                line = line.rstrip() + ':'
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
    """Fix all Mojo files in the project."""
    project_root = "/Users/ryan_david_oates/cognitive-design-framework"
    
    # Find all .mojo files
    mojo_files = []
    for root, dirs, files in os.walk(project_root):
        for file in files:
            if file.endswith('.mojo'):
                mojo_files.append(os.path.join(root, file))
    
    print(f"Found {len(mojo_files)} Mojo files to process...")
    
    fixed_count = 0
    for filepath in mojo_files:
        if fix_mojo_file(filepath):
            print(f"Fixed: {filepath}")
            fixed_count += 1
    
    print(f"\nFixed {fixed_count} files out of {len(mojo_files)} total files.")
    print("Run 'pixi run format' again to see if issues are resolved.")

if __name__ == "__main__":
    main()
