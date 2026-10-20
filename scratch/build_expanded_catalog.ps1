# Script to expand catalog.js to 325+ verified titles
$baseCatalogScript = Get-Content -Raw "catalog.js"

# Let's inspect how many titles are currently in catalog.js
$currentMatches = [regex]::Matches($baseCatalogScript, 'id:\s*"([^"]+)"')
Write-Host "Current count in catalog.js: $($currentMatches.Count)"
