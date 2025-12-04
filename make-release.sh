#!/bin/bash

# Require being on develop branch
current_branch=$(git rev-parse --abbrev-ref HEAD)
if [ "$current_branch" != "develop" ]; then
  echo "You must be on the 'develop' branch to run this script."
  exit 1
fi

# Ensure an argument is provided (major|minor|patch)
if [ -z "$1" ]; then
  echo "Usage: $0 <major|minor|patch>"
  exit 1
fi

# Read existing version from version.txt
if [ ! -f version.txt ]; then
  echo "version.txt not found!"
  exit 1
fi

version=$(cat version.txt)

# Strip leading 'v' if present
clean_version=${version#v}

# Split into components
IFS='.' read -r major minor patch <<< "$clean_version"

# Increment based on argument
case "$1" in
  major)
    major=$((major + 1))
    minor=0
    patch=0
    ;;
  minor)
    minor=$((minor + 1))
    patch=0
    ;;
  patch)
    patch=$((patch + 1))
    ;;
  *)
    echo "Argument must be: major | minor | patch"
    exit 1
    ;;
esac

# Rebuild version and prepend v
version="v$major.$minor.$patch"

# Update version.txt and commit it ---
echo "$version" > version.txt
git add version.txt
git commit -m "- Update version.txt"

# Get commits since last tag in reverse order (oldest first)
release_notes=$(git log $(git describe --tags --abbrev=0)..HEAD --pretty=format:"%s (%h)" --reverse)

# Build the tag message
tag_message="Release $version

$release_notes"

# Show the release notes to the user
echo "==== Release Notes for $version ===="
echo "$tag_message"
echo "==================================="

# Ask for confirmation
read -p "Do you want to create this tag and create a release branch? (y/N): " confirm

if [[ "$confirm" =~ ^[Yy]$ ]]; then
  # Create annotated tag
  git tag -a "$version" -m "$tag_message"
  git checkout -b release/$version

  echo "Don't forget to push the branch and tag:"
  echo "git push"
  echo "git push origin $version"
else
  echo "Tagging cancelled."
fi