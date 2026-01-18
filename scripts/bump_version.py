#!/usr/bin/env python3
"""Script to bump version across all project files."""
import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path


def get_current_version(manifest_path: Path) -> str:
    """Get current version from manifest.json."""
    with open(manifest_path, "r") as f:
        manifest = json.load(f)
    return manifest["version"]


def bump_version(version: str, bump_type: str) -> str:
    """Bump version according to semver."""
    major, minor, patch = map(int, version.split("."))
    
    if bump_type == "major":
        return f"{major + 1}.0.0"
    elif bump_type == "minor":
        return f"{major}.{minor + 1}.0"
    elif bump_type == "patch":
        return f"{major}.{minor}.{patch + 1}"
    else:
        raise ValueError(f"Invalid bump type: {bump_type}")


def update_manifest(manifest_path: Path, new_version: str) -> None:
    """Update version in manifest.json."""
    with open(manifest_path, "r") as f:
        manifest = json.load(f)
    
    manifest["version"] = new_version
    
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")
    
    print(f"✓ Updated manifest.json: {new_version}")


def update_readme(readme_path: Path, new_version: str) -> None:
    """Update version in README.md."""
    with open(readme_path, "r") as f:
        content = f.read()
    
    # Update the Current version line
    pattern = r"Current version: \*\*[\d.]+\*\*"
    replacement = f"Current version: **{new_version}**"
    
    if re.search(pattern, content):
        content = re.sub(pattern, replacement, content)
        
        with open(readme_path, "w") as f:
            f.write(content)
        
        print(f"✓ Updated README.md: {new_version}")
    else:
        print("⚠ Warning: Could not find version line in README.md")


def prepare_changelog_entry(changelog_path: Path, new_version: str, changes: str) -> None:
    """Add new version entry to CHANGELOG.md."""
    with open(changelog_path, "r") as f:
        lines = f.readlines()
    
    # Find the position to insert the new entry (after the header)
    insert_pos = 0
    for i, line in enumerate(lines):
        if line.startswith("## ["):
            insert_pos = i
            break
    
    # Create new entry
    date = datetime.now().strftime("%Y-%m-%d")
    new_entry = [
        f"## [{new_version}] - {date}\n",
        "\n",
    ]
    
    # Add the changes if provided
    if changes:
        new_entry.extend([
            f"{changes}\n",
            "\n",
        ])
    else:
        new_entry.extend([
            "### Changed\n",
            "- [Add your changes here]\n",
            "\n",
        ])
    
    # Insert the new entry
    lines[insert_pos:insert_pos] = new_entry
    
    with open(changelog_path, "w") as f:
        f.writelines(lines)
    
    print(f"✓ Updated CHANGELOG.md with version {new_version}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Bump version across project files")
    parser.add_argument(
        "bump_type",
        choices=["major", "minor", "patch"],
        help="Type of version bump (major, minor, or patch)",
    )
    parser.add_argument(
        "--version",
        help="Specific version to set (overrides bump_type calculation)",
    )
    parser.add_argument(
        "--changes",
        help="Brief description of changes for CHANGELOG.md",
        default="",
    )
    parser.add_argument(
        "--no-changelog",
        action="store_true",
        help="Skip updating CHANGELOG.md",
    )
    
    args = parser.parse_args()
    
    # Define paths
    root_dir = Path(__file__).parent.parent
    manifest_path = root_dir / "custom_components" / "juno_rb56sc" / "manifest.json"
    readme_path = root_dir / "README.md"
    changelog_path = root_dir / "CHANGELOG.md"
    
    # Check if files exist
    if not manifest_path.exists():
        print(f"❌ Error: manifest.json not found at {manifest_path}")
        sys.exit(1)
    
    # Get current version
    current_version = get_current_version(manifest_path)
    print(f"Current version: {current_version}")
    
    # Calculate new version
    if args.version:
        new_version = args.version
    else:
        new_version = bump_version(current_version, args.bump_type)
    
    print(f"New version: {new_version}")
    
    # Update files
    update_manifest(manifest_path, new_version)
    
    if readme_path.exists():
        update_readme(readme_path, new_version)
    else:
        print("⚠ Warning: README.md not found")
    
    if not args.no_changelog and changelog_path.exists():
        prepare_changelog_entry(changelog_path, new_version, args.changes)
    elif not changelog_path.exists():
        print("⚠ Warning: CHANGELOG.md not found")
    
    print(f"\n✅ Version bumped successfully from {current_version} to {new_version}")
    print("\n📝 Next steps:")
    print("   1. Review and update CHANGELOG.md with detailed changes")
    print("   2. Commit the changes: git add . && git commit -m 'Bump version to {}'".format(new_version))
    print("   3. Create a git tag: git tag v{}".format(new_version))
    print("   4. Push changes: git push && git push --tags")


if __name__ == "__main__":
    main()
