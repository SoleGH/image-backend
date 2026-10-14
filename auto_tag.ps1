param(
  [string]$ProjectSubdir = "project"
)
$ErrorActionPreference = "Stop"
$root = $PSScriptRoot

# 1. Pull remote code
Write-Host "Pulling remote code..."
git pull

# 4. Commit all changes
Write-Host "Checking for changes..."
$changes = git status --porcelain
if ($changes) {
    Write-Host "Committing changes..."
    git add -A
    git commit -m "chore: auto deploy"
} else {
    Write-Host "No changes to commit."
}

# 5. Tag
Write-Host "Calculating next tag..."
# Get remote tags to ensure we don't conflict and satisfy "get remote latest tag"
$remoteTags = git ls-remote --tags origin
$versions = @()
foreach ($line in $remoteTags) {
    if ($line -match "refs/tags/v(\d+\.\d+\.\d+)$") {
        try {
            $ver = [Version]$Matches[1]
            $versions += $ver
        } catch {
            Write-Warning "Skipping invalid tag format: $($Matches[0])"
        }
    }
}

if ($versions.Count -eq 0) {
    $newTag = "v0.0.0"
} else {
    $latest = ($versions | Sort-Object -Descending | Select-Object -First 1)
    $newTag = "v{0}.{1}.{2}" -f $latest.Major, $latest.Minor, ($latest.Build + 1)
}

Write-Host "New tag: $newTag"
git tag -a $newTag -m "release $newTag"

# 6. Push
Write-Host "Pushing to remote..."
git push
git push origin $newTag

Write-Host "Done."
