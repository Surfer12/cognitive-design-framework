#!/usr/bin/env python3
"""
Enhanced script to fix remaining Mojo syntax issues.
"""

import os
import re
import glob

def fix_mojo_file_v2(filepath):
    """Fix additional syntax issues in a single Mojo file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix 1: Add missing parameters to function definitions
        content = re.sub(
            r'fn (\w+)\(\) -> (\w+) raises:',
            r'fn \1(inout self) -> \2 raises:',
            content
        )
        
        # Fix 2: Add missing parameters to function definitions without raises
        content = re.sub(
            r'fn (\w+)\(\) -> (\w+) $',
            r'fn \1(inout self) -> \2:',
            content,
            flags=re.MULTILINE
        )
        
        # Fix 3: Fix function signatures with trailing spaces
        content = re.sub(
            r'fn (\w+)\([^)]*\) -> (\w+) $',
            r'fn \1(inout self) -> \2:',
            content,
            flags=re.MULTILINE
        )
        
        # Fix 4: Fix accept method with incomplete signature
        content = re.sub(
            r'fn accept\(inout self, visitor: (\w+)\) -> None$',
            r'fn accept(inout self, visitor: \1):',
            content,
            flags=re.MULTILINE
        )
        
        # Fix 5: Fix visitor methods without self parameter
        content = re.sub(
            r'fn visit_attribute\(attribute: (\w+)\):$',
            r'fn visit_attribute(inout self, attribute: \1):',
            content,
            flags=re.MULTILINE
        )
        
        # Fix 6: Fix let declarations in function bodies
        content = re.sub(
            r'(\s+)let (\w+) = (.+)$',
            r'\1var \2 = \3',
            content,
            flags=re.MULTILINE
        )
        
        # Fix 7: Fix enum declarations
        content = re.sub(
            r'enum (\w+):$',
            r'@value\nstruct \1:',
            content,
            flags=re.MULTILINE
        )
        
        # Fix 8: Fix standalone function definitions
        content = re.sub(
            r'^fn (\w+)\(([^)]*)\) -> (\w+) $',
            r'fn \1(\2) -> \3:',
            content,
            flags=re.MULTILINE
        )
        
        # Fix 9: Fix isa operator
        content = re.sub(
            r'if (\w+) isa (\w+):',
            r'if isinstance(\1, \2):',
            content
        )
        
        # Fix 10: Fix alias declarations
        content = re.sub(
            r'let (\w+) = "([^"]*)"$',
            r'alias \1 = "\2"',
            content,
            flags=re.MULTILINE
        )
        
        # Fix 11: Fix indentation issues by normalizing
        lines = content.split('\n')
        fixed_lines = []
        
        for i, line in enumerate(lines):
            # Skip empty lines
            if not line.strip():
                fixed_lines.append(line)
                continue
                
            # Fix common indentation patterns
            if line.strip().startswith('fn ') and not line.endswith(':'):
                line = line.rstrip() + ':'
            
            # Fix function calls in let statements
            if 'let ' in line and '(' in line and ')' in line:
                line = line.replace('let ', 'var ')
            
            fixed_lines.append(line)
        
        content = '\n'.join(fixed_lines)
        
        # Fix 12: Remove duplicate pass statements
        content = re.sub(r'(\s+pass\s*\n)+', r'\1', content)
        
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
        if fix_mojo_file_v2(filepath):
            print(f"Fixed: {filepath}")
            fixed_count += 1
    
    print(f"\nFixed {fixed_count} files out of {len(mojo_files)} total files.")
    print("Run 'pixi run format' again to see if more issues are resolved.")

if __name__ == "__main__":
    main()
