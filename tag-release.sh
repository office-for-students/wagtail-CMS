#!/bin/bash

# Ensure a version argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <version>"
  exit 1
fi

version=$1

# Prepend 'v' if not already present
if [[ "$version" != v* ]]; then
  version="v$version"
fi

# Update version.txt and commit it ---
echo "$version" > version.txt
git add version.txt
git commit -m "Update version.txt"

# Get commits since last tag in reverse order (oldest first)
release_notes=$(git log $(git describe --tags --abbrev=0)..HEAD --pretty=format:"- %s (%an)" --reverse)

# Build the tag message
tag_message="Release $version

$release_notes"

# Show the release notes to the user
echo "==== Release Notes for $version ===="
echo "$tag_message"
echo "==================================="

# Ask for confirmation
read -p "Do you want to push this tag? (y/N): " confirm

if [[ "$confirm" =~ ^[Yy]$ ]]; then
  # Create annotated tag
  git tag -a "$version" -m "$tag_message"

  # Push both the new commit and tag
  git push origin HEAD
  git push origin "$version"
  echo "Tag $version pushed successfully."
else
  echo "Tagging cancelled."
fi
