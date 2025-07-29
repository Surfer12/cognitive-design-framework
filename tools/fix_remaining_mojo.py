# tools/fix_remaining_mojo.py
import os
import re
from typing import List

PROJECT_ROOT = "/Users/ryan_david_oates/cognitive-design-framework"

def find_mojo_files(root: str) -> List[str]:
    """Find all .mojo files in the project."""
    mojo_files = []
    for dirpath, _, filenames in os.walk(root):
        for fname in filenames:
            if fname.endswith('.mojo'):
                mojo_files.append(os.path.join(dirpath, fname))
    return mojo_files

def fix_enum_syntax(content: str) -> str:
    """Fix enum syntax to proper Mojo format."""
    # Replace C-style enums with Mojo enum blocks
    content = re.sub(r'enum\s+([A-Za-z_]+)\s*{([^}]*)}', r'enum \1:\n\2', content)
    return content

def fix_generic_functions(content: str) -> str:
    """Add missing colons and type hints in generic functions."""
    # Simple pattern to add colon after fn name(params)
    content = re.sub(r'fn\s+([A-Za-z_]+)\s*\(([^)]*)\)', r'fn \1(\2):', content)
    return content

def fix_indentation(content: str) -> str:
    """Normalize indentation to 4 spaces."""
    lines = content.split('\n')
    fixed_lines = []
    for line in lines:
        # Replace tabs with 4 spaces
        fixed_line = line.replace('\t', '    ')
        fixed_lines.append(fixed_line)
    return '\n'.join(fixed_lines)

def fix_stubbed_functions(content: str) -> str:
    """Add pass to empty function bodies."""
    # Add pass to fn ... : without body
    content = re.sub(r'fn\s+.*:\s*$', r'\1\n    pass', content, flags=re.MULTILINE)
    return content

def process_file(filepath: str) -> bool:
    """Process a single Mojo file and apply fixes."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    original = content
    content = fix_enum_syntax(content)
    content = fix_generic_functions(content)
    content = fix_indentation(content)
    content = fix_stubbed_functions(content)
    
    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        return True
    return False

def main():
    """Main function to fix all Mojo files."""
    mojo_files = find_mojo_files(PROJECT_ROOT)
    fixed_count = 0
    for file in mojo_files:
        if process_file(file):
            print(f"Fixed: {file}")
            fixed_count += 1
    print(f"Total files fixed: {fixed_count} out of {len(mojo_files)}")

if __name__ == "__main__":
    main()