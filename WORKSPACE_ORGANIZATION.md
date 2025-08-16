# Workspace Organization Plan

## Current State Analysis
The workspace contains:
- 100+ files scattered in the root directory
- Multiple demo files with similar functionality
- Duplicate implementations (Python and Mojo versions)
- Mixed documentation and code files
- Inconsistent naming conventions

## Target Structure (Based on README)
```
cognitive-design-framework/
├── core/                    # Fundamental cognitive processing components
│   ├── base/               # Base interfaces and structures
│   ├── bridge/             # Cognitive bridge implementations
│   ├── autopoietic/        # Autopoietic system components
│   └── structures/         # Core cognitive structures
├── systems/                # Specific system implementations
│   ├── autopoietic/        # Autopoietic systems
│   ├── consciousness/      # Consciousness frameworks
│   └── mecn/              # MECN implementations
├── tools/                  # Utility and optimization tools
│   ├── analysis/          # Complexity and performance analysis
│   ├── refactoring/       # Code refactoring utilities
│   └── validation/        # Testing and validation tools
├── docs/                   # Comprehensive documentation
│   ├── architecture/       # System architecture docs
│   ├── theoretical/        # Theoretical foundations
│   ├── api/               # API documentation
│   └── guides/            # User guides and tutorials
├── examples/               # Usage examples and tutorials
│   ├── basic/             # Basic usage examples
│   ├── advanced/          # Advanced implementations
│   └── demos/             # Demonstration files
├── tests/                  # Comprehensive test suites
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   └── performance/       # Performance tests
├── config/                 # Configuration management
├── archive/               # Archived/deprecated files
└── scripts/               # Build and utility scripts
```

## Organization Actions

### Phase 1: Create Directory Structure
- Create missing directories
- Establish proper hierarchy

### Phase 2: Categorize and Move Files
- Group similar files together
- Move demo files to examples/
- Organize documentation
- Archive outdated files

### Phase 3: Clean Up Root Directory
- Keep only essential files in root
- Move configuration files to config/
- Consolidate similar implementations

### Phase 4: Update References
- Update import statements
- Fix relative paths
- Update documentation links

## File Categories

### Core Framework Files (keep in root)
- README.md
- CONTRIBUTING.md
- CODE_OF_CONDUCT.md
- LICENSE files
- .gitignore
- .gitattributes

### Configuration Files (move to config/)
- pixi.toml
- pixi.lock
- magic.lock
- .mojoformat

### Demo Files (move to examples/demos/)
- All *_demo.* files
- All *_working_*.* files
- All minimal_*.* files

### Documentation (organize in docs/)
- All .md files except root-level
- Architecture documents
- Theoretical foundations

### Tools and Scripts (move to tools/)
- All fix_*.py files
- Refactoring scripts
- Analysis tools

### Archive (move to archive/)
- Duplicate implementations
- Outdated files
- Experimental code

## Implementation Priority
1. Create directory structure
2. Move configuration files
3. Organize demo files
4. Clean up documentation
5. Archive outdated files
6. Update references
