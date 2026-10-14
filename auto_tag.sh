#!/bin/bash
set -e

# 1. Pull remote code
echo "Pulling remote code..."
git pull

# 4. Commit all changes
echo "Checking for changes..."
if [ -n "$(git status --porcelain)" ]; then
    echo "Committing changes..."
    git add -A
    git commit -m "chore: auto deploy"
else
    echo "No changes to commit."
fi

# 5. Tag
echo "Calculating next tag..."
# Get remote tags
remote_tags=$(git ls-remote --tags origin | grep -o 'refs/tags/v[0-9]*\.[0-9]*\.[0-9]*$' | sed 's|refs/tags/||')

if [ -z "$remote_tags" ]; then
    new_tag="v0.0.0"
else
    # Sort tags by version logic
    # Remove 'v', replace dots with spaces, sort numerically, take last
    latest_tag=$(echo "$remote_tags" | sed 's/^v//' | sort -t. -k1,1n -k2,2n -k3,3n | tail -n 1)
    
    # Split into array
    IFS='.' read -r major minor patch <<< "$latest_tag"
    
    # Increment patch
    patch=$((patch + 1))
    new_tag="v$major.$minor.$patch"
fi

echo "New tag: $new_tag"
git tag -a "$new_tag" -m "release $new_tag"

# 6. Push
echo "Pushing to remote..."
git push
git push origin "$new_tag"

echo "Done."
