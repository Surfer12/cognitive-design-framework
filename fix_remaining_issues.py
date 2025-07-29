#!/usr/bin/env python3
"""Fix remaining Mojo syntax issues."""

import os
import re
from pathlib import Path

def fix_remaining_issues(filepath):
    """Fix remaining syntax issues in Mojo files."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix 1: Remove "alias" from variable declarations
        content = re.sub(r'var (\w+): alias (\w+) = ""', r'var \1: \2', content)
        
        # Fix 2: Fix malformed struct declarations
        content = re.sub(r'struct (\w+):var (\w+): alias (\w+) = ""', r'struct \1:\n    var \2: \3', content)
        
        # Fix 3: Fix function declarations with missing newlines
        content = re.sub(r'fn (\w+)\(\):"""([^"]+)"""', r'fn \1():\n    """\2"""', content)
        content = re.sub(r'fn (\w+)\([^)]*\):"""([^"]+)"""', r'fn \1():\n    """\2"""', content)
        
        # Fix 4: Fix enum declarations
        content = re.sub(r'(\s+)enum (\w+):', r'\1@value\n\1struct \2:', content)
        
        # Fix 5: Fix trait declarations
        content = re.sub(r'trait (\w+):', r'struct \1:', content)
        
        # Fix 6: Fix let/var issues in function bodies
        content = re.sub(r'let (\w+) = ([^\n]+)', r'var \1 = \2', content)
        
        # Fix 7: Fix Python import issues
        content = re.sub(r'var (\w+): PythonObject  # Python dict for thread-safe alias storage = ""', 
                        r'var \1: PythonObject', content)
        content = re.sub(r'var (\w+): PythonObject  # Python dict for thread-safe storage alias (\w+) = ""', 
                        r'var \1: PythonObject', content)
        
        # Fix 8: Clean up malformed lines
        lines = content.split('\n')
        fixed_lines = []
        
        for i, line in enumerate(lines):
            # Skip completely malformed lines
            if '<line number missing in source>' in line:
                continue
                
            # Fix struct declarations that got mangled
            if line.strip().startswith('struct') and ':var' in line:
                parts = line.split(':var')
                if len(parts) == 2:
                    struct_part = parts[0].strip()
                    var_part = parts[1].strip()
                    fixed_lines.append(struct_part + ':')
                    if var_part:
                        var_part = re.sub(r' alias (\w+) = ""', '', var_part)
                        fixed_lines.append('    var ' + var_part)
                    continue
            
            # Fix function parameter issues
            if 'fn ' in line and ') -> None raises:' in line:
                line = re.sub(r'fn (\w+)\(inout self\) -> None raises:', r'fn \1(inout self) raises:', line)
            
            fixed_lines.append(line)
        
        content = '\n'.join(fixed_lines)
        
        # Fix 9: Remove empty alias assignments
        content = re.sub(r'alias (\w+) = ""\n', '', content)
        
        # Fix 10: Clean up multiple newlines
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    """Fix remaining issues in all Mojo files."""
    project_root = Path("/Users/ryan_david_oates/cognitive-design-framework")
    
    # Find all .mojo files
    mojo_files = list(project_root.rglob("*.mojo"))
    
    print(f"Found {len(mojo_files)} Mojo files to fix...")
    
    fixed_count = 0
    for filepath in mojo_files:
        if fix_remaining_issues(filepath):
            print(f"Fixed: {filepath}")
            fixed_count += 1
    
    print(f"\nFixed {fixed_count} files.")

if __name__ == "__main__":
    main()