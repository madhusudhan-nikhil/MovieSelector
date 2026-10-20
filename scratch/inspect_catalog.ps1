$titles = Get-Content 'catalog.js' | Select-String 'title:\s*"([^"]+)"' | ForEach-Object { $_.Matches[0].Groups[1].Value }
Write-Host "Total titles in catalog.js: $($titles.Count)"

$poolTitles = Get-Content 'index.html' | Select-String 'title:\s*"([^"]+)"' | Where-Object { $_.LineNumber -gt 1627 -and $_.LineNumber -lt 2650 } | ForEach-Object { $_.Matches[0].Groups[1].Value }
Write-Host "Total titles in freshPullPool: $($poolTitles.Count)"

$totalUniq = ($titles + $poolTitles | Select-Object -Unique).Count
Write-Host "Total Unique Combined: $totalUniq"
