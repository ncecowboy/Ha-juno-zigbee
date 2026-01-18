# Version Management Guide

This document describes the automated version management system for the Juno RB56SC Zigbee Light integration.

## Overview

The project uses [Semantic Versioning](https://semver.org/) (SemVer) for version numbering:
- **MAJOR** version (X.0.0): Breaking changes that require user action
- **MINOR** version (0.X.0): New features, backward compatible
- **PATCH** version (0.0.X): Bug fixes, backward compatible

## Automated Version Bumping

### How It Works

When a Pull Request is merged to the `main` or `master` branch, the version is automatically bumped based on:

1. **PR Labels** (highest priority):
   - `major` or `breaking`: Bumps MAJOR version
   - `minor`, `feature`, or `enhancement`: Bumps MINOR version
   - `patch`, `fix`, `bugfix`, or `bug`: Bumps PATCH version

2. **PR Title** (fallback):
   - Starting with `feat:`, `feature:`, `enhancement:`: Bumps MINOR version
   - Starting with `fix:`, `bugfix:`, `patch:`: Bumps PATCH version
   - Starting with `breaking:`, `major:`: Bumps MAJOR version

3. **Default**: If no labels or title match, defaults to PATCH version bump

### What Gets Updated

The automation updates these files:
- `custom_components/juno_rb56sc/manifest.json` - Integration version
- `README.md` - Current version section
- `CHANGELOG.md` - Adds new version entry with changes

### Workflow

1. Developer creates a PR with appropriate labels
2. PR is reviewed and merged
3. GitHub Actions workflow automatically:
   - Determines the version bump type
   - Runs the `scripts/bump_version.py` script
   - Updates all version files
   - Creates a changelog entry with PR title
   - Commits and pushes the changes
   - Creates and pushes a git tag (e.g., `v1.2.1`)

## Manual Version Bumping

You can also manually bump the version using the provided script:

### Basic Usage

```bash
# Bump patch version (1.2.0 → 1.2.1)
python3 scripts/bump_version.py patch

# Bump minor version (1.2.0 → 1.3.0)
python3 scripts/bump_version.py minor

# Bump major version (1.2.0 → 2.0.0)
python3 scripts/bump_version.py major
```

### Advanced Usage

```bash
# Set a specific version
python3 scripts/bump_version.py patch --version 1.5.0

# Add custom changelog entry
python3 scripts/bump_version.py minor --changes "### Added
- New feature X
- New feature Y

### Fixed
- Bug Z"

# Skip changelog update
python3 scripts/bump_version.py patch --no-changelog
```

### Manual Process

After running the script manually:

1. Review the updated `CHANGELOG.md` and add detailed changes
2. Commit the changes:
   ```bash
   git add .
   git commit -m "chore: bump version to X.Y.Z"
   ```
3. Create and push a git tag:
   ```bash
   git tag vX.Y.Z
   git push && git push --tags
   ```

## Changelog Guidelines

### Format

The CHANGELOG.md follows [Keep a Changelog](https://keepachangelog.com/) format with these sections:

- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security fixes

### Writing Good Changelog Entries

**Good examples:**
```markdown
### Fixed
- Fixed AttributeError when setting up multiple devices simultaneously (#123)
- Corrected device name display in configuration flow

### Added
- Support for ABL-LIGHT-Z-201 model
- Multi-device selection during setup

### Changed
- Improved error messaging for device selection scenarios
```

**Bad examples:**
```markdown
### Fixed
- Fixed bug
- Updated code

### Added
- New stuff
```

### Detailed Notes Requirements

Each changelog entry should include:

1. **What changed**: Clear description of the change
2. **Why it changed**: Context or problem being solved (if not obvious)
3. **Impact**: How it affects users (breaking changes, new features, etc.)
4. **References**: PR/issue numbers when applicable

**Example of detailed entry:**
```markdown
## [1.2.1] - 2026-01-18

### Fixed
- Fixed AttributeError when setting up multiple devices at once (#42)
  - The configuration flow now properly handles multi-device selection
  - Additional devices are configured through separate import flows
  - Resolves crash that occurred when users selected multiple devices during setup
  - Impact: Users can now successfully configure multiple Juno devices in one session

### Technical
- Removed incorrect call to `self.hass.config_entries.async_create_entry()`
- Added `async_step_import()` method for programmatic device setup
- Improved code review feedback implementation
```

## Best Practices

### For Contributors

1. **Label your PRs appropriately**:
   - Use `fix` label for bug fixes
   - Use `feature` or `enhancement` for new features
   - Use `breaking` for breaking changes

2. **Write descriptive PR titles**:
   - Good: `fix: resolve AttributeError in multi-device setup`
   - Bad: `update config_flow.py`

3. **Include details in PR description**:
   - What problem does this solve?
   - What changes were made?
   - How to test the changes?

### For Maintainers

1. **Review changelog entries** after automated bumps to ensure they're detailed enough
2. **Edit changelog** if the automated entry needs more context
3. **Create GitHub releases** from the tags with release notes copied from changelog

## Release Process

1. PR is merged → version auto-bumped → tag created
2. Tag creation triggers Release workflow (`.github/workflows/release.yml`)
3. Release workflow:
   - Updates manifest.json with version from tag
   - Creates a zip file of the integration
   - Uploads zip as release asset
4. Maintainer adds release notes from CHANGELOG.md to GitHub release

## Troubleshooting

### Version not bumped after PR merge

Check:
- PR was actually merged (not just closed)
- Workflow has necessary permissions (`contents: write`)
- Check workflow run logs in GitHub Actions

### Incorrect version bump type

- Ensure PR has correct labels
- Check PR title follows conventional commit format
- Manually adjust if needed using the script

### Changelog entry missing details

- Edit CHANGELOG.md manually to add more details
- Commit with: `git commit -m "docs: improve changelog entry"`

## Files Managed by Version System

- `custom_components/juno_rb56sc/manifest.json` - Integration version (required by Home Assistant)
- `README.md` - "Current version" section for documentation
- `CHANGELOG.md` - Version history and changes

## Version Validation

The HACS validation and Home Assistant Hassfest workflows verify:
- Version format is valid (X.Y.Z)
- manifest.json is properly formatted
- Version matches expected format for Home Assistant integrations
