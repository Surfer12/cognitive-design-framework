# Organization Strategy

## Phased Directory Structure

### Phase 1: Minimal Restructuring
```
cognitive-design-framework/
├── core/                      # Move from examples/core
│   ├── base/
│   │   ├── tag_element.mojo
│   │   └── visitor.mojo
│   ├── bridge/
│   │   └── cognitive_bridge.mojo
│   └── __init__.mojo
├── systems/                   # Move from examples/autopoietic
│   ├── autopoietic/
│   │   ├── system.mojo
│   │   └── test_system.mojo
│   └── __init__.mojo
├── examples/                  # Keep for backward compatibility
│   └── legacy_imports.mojo    # Redirect to new locations
└── docs/
    ├── README.md
    ├── THEORETICAL_FOUNDATIONS.md
    ├── NEXT_STEPS.md
    └── PROGRESS_AND_FOCUS.md
```

### Phase 2: Feature Integration
```
cognitive-design-framework/
├── core/
│   ├── meta/                 # New metacognitive features
│   │   ├── reflection.mojo
│   │   └── monitoring.mojo
│   └── patterns/            # New pattern recognition
│       ├── detector.mojo
│       └── analyzer.mojo
├── systems/
│   ├── autopoietic/
│   └── integration/         # New integration features
└── tools/                   # New tool integration
    ├── discovery/
    └── optimization/
```

## Gentle Migration Strategy

### 1. Create Symbolic Links
```bash
# Create new directories without moving files
mkdir -p core/{base,bridge}
mkdir -p systems/autopoietic

# Create symbolic links first
ln -s examples/core/tag_element.mojo core/base/
ln -s examples/core/visitor.mojo core/base/
```

### 2. Update Import Statements
```mojo
# Old import
from ..core.tag_element import TagElement

# New import (with compatibility layer)
from cognitive_design_framework.core.base.tag_element import TagElement
# or
from ..legacy_imports import TagElement  # For backward compatibility
```

### 3. Gradual File Migration
```yaml
migration_steps:
  - step: "Create new directory structure"
    impact: "None - just creates empty directories"

  - step: "Add symbolic links"
    impact: "None - maintains existing imports"

  - step: "Copy files to new locations"
    impact: "None - files exist in both places"

  - step: "Update imports in new files"
    impact: "Minimal - only affects new code"

  - step: "Deprecate old locations"
    impact: "None - just adds warnings"
```

## Implementation Plan

### Week 1: Setup
- [ ] Create new directory structure
- [ ] Add symbolic links
- [ ] Create compatibility layer

### Week 2: Core Migration
- [ ] Move core components
- [ ] Update import statements
- [ ] Add deprecation warnings

### Week 3: Systems Migration
- [ ] Move system components
- [ ] Update documentation
- [ ] Test all functionality

## File Renaming Strategy

### 1. Use Temporary Bridges
```mojo
# bridge_imports.mojo
from .new_name import NewClass as OldClass
```

### 2. Gradual Class Renaming
```mojo
# Phase 1: Add new name
class NewClassName(OldClassName):
    """New implementation with same interface."""
    pass

# Phase 2: Deprecate old name
class OldClassName:
    """@deprecated: Use NewClassName instead."""
    def __init__(self):
        warn("OldClassName is deprecated")
```

## Documentation Updates

### 1. Import Path Updates
```markdown
## Updated Import Paths

Old:
```mojo
from examples.core.tag_element import TagElement
```

New:
```mojo
from cognitive_design_framework.core.base.tag_element import TagElement
```
```

### 2. Directory Structure Documentation
```markdown
Keep both old and new paths documented until migration is complete:

- Old: `examples/core/tag_element.mojo`
- New: `core/base/tag_element.mojo`
```

## Testing Strategy

### 1. Parallel Test Suites
```yaml
test_strategy:
  old_paths:
    - location: "tests/legacy/"
    - maintain: true
    - deprecation: "Warn but don't fail"

  new_paths:
    - location: "tests/current/"
    - enforce: true
    - coverage: "Required"
```

### 2. Import Validation
```mojo
fn validate_imports():
    """Ensure all imports follow new structure."""
    # Check import patterns
    # Warn on deprecated paths
    # Suggest updates
```

## Risk Mitigation

### 1. Backup Strategy
```bash
# Create backups before each phase
cp -r cognitive-design-framework cognitive-design-framework.bak-phase1
```

### 2. Rollback Plan
```yaml
rollback_steps:
  - restore_files: "Restore from backup"
  - revert_imports: "Use old import paths"
  - remove_links: "Clean up symbolic links"
```

### 3. Version Control
```bash
# Create feature branches for each phase
git checkout -b reorganization/phase1
git checkout -b reorganization/phase2
```

## Success Metrics

### 1. Code Health
- No broken imports
- All tests passing
- Documentation up to date

### 2. Performance
- No degradation in load times
- Maintained system performance
- Efficient import resolution

### 3. Developer Experience
- Clear file organization
- Intuitive import paths
- Minimal disruption

## Next Actions

### Today
1. Create new directory structure
2. Setup symbolic links
3. Create compatibility layer

### This Week
1. Begin core component migration
2. Update primary import paths
3. Add initial documentation

### Next Week
1. Complete file migrations
2. Update remaining imports
3. Remove deprecated paths
