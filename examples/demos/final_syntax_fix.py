#!/usr/bin/env python3
"""Final comprehensive fix for Mojo syntax issues."""

import re
from pathlib import Path

def fix_final_issues(filepath):
    """Apply final fixes to Mojo files."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix struct declarations without proper body
        lines = content.split('\n')
        fixed_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Skip malformed lines
            if '<line number missing in source>' in line:
                i += 1
                continue
            
            # Fix struct declarations
            if line.strip().startswith('struct ') and line.strip().endswith(':'):
                fixed_lines.append(line)
                # Add pass if next line doesn't start with proper indentation
                if i + 1 < len(lines):
                    next_line = lines[i + 1]
                    if not next_line.strip() or not next_line.startswith('    '):
                        fixed_lines.append('    pass')
                else:
                    fixed_lines.append('    pass')
                i += 1
                continue
            
            # Fix variable declarations at module level
            if re.match(r'^\s*var \w+:', line) and not line.strip().endswith('='):
                # Add default value
                if ': String' in line:
                    line = line.rstrip() + ' = ""'
                elif ': Float64' in line:
                    line = line.rstrip() + ' = 0.0'
                elif ': Int' in line:
                    line = line.rstrip() + ' = 0'
                elif ': PythonObject' in line:
                    line = line.rstrip() + ' = Python.none()'
            
            # Fix function declarations without body
            if re.match(r'^\s*fn \w+\([^)]*\):', line):
                fixed_lines.append(line)
                # Check if next line has proper body
                if i + 1 < len(lines):
                    next_line = lines[i + 1]
                    if not next_line.strip() or not next_line.startswith('    '):
                        fixed_lines.append('    pass')
                else:
                    fixed_lines.append('    pass')
                i += 1
                continue
            
            # Fix malformed function signatures
            if '](inout self(inout self' in line:
                # This is a malformed line, try to fix it
                line = re.sub(r'](inout self\(inout self.*', '(inout self):', line)
            
            # Fix docstring issues
            if line.strip() == '"""' and i > 0:
                prev_line = lines[i-1].strip()
                if not prev_line.startswith('"""') and not prev_line.endswith('"""'):
                    # This is a standalone closing docstring, skip it
                    i += 1
                    continue
            
            # Fix list/tuple syntax issues
            if line.strip().startswith('"') and line.strip().endswith('",'):
                # This looks like a malformed list item
                if not any(x in line for x in ['[', '(', '=']):
                    i += 1
                    continue
            
            fixed_lines.append(line)
            i += 1
        
        content = '\n'.join(fixed_lines)
        
        # Additional regex fixes
        content = re.sub(r'var (\w+): PythonObject  # Python dict for thread-safe state\s+fn', 
                        r'var \1: PythonObject\n\n    fn', content)
        
        # Fix Python method calls
        content = re.sub(r'Python\.dict\(\)', 'Python.dict()', content)
        
        # Clean up multiple newlines
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
    """Apply final fixes to all Mojo files."""
    project_root = Path("/Users/ryan_david_oates/cognitive-design-framework")
    
    # Find all .mojo files
    mojo_files = list(project_root.rglob("*.mojo"))
    
    print(f"Applying final fixes to {len(mojo_files)} Mojo files...")
    
    fixed_count = 0
    for filepath in mojo_files:
        if fix_final_issues(filepath):
            print(f"Fixed: {filepath}")
            fixed_count += 1
    
    print(f"\nApplied final fixes to {fixed_count} files.")

if __name__ == "__main__":
    main()