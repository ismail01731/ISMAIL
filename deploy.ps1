$ErrorActionPreference = "Stop"
Set-Location "D:\ISMAIL"
Write-Host ""
Write-Host "========================================"
Write-Host "        ISMAIL AI ONLINE DEPLOY"
Write-Host "========================================"
Write-Host ""
# Stage only frontend and backend production changes
git add frontend backend
# Remove backup/test files from staging
$stagedFiles = git diff --cached --name-only -- frontend backend
foreach ($file in $stagedFiles) {
    if (
        $file -match "backup" -or
        $file -match "\.task[0-9]+-" -or
        $file -match "_task[0-9]+_" -or
        $file -match "test_" -or
        $file -match "\.txt$"
    ) {
        git restore --staged -- "$file"
    }
}
# Read final list of files to deploy
$changes = git diff --cached --name-only -- frontend backend
if (-not $changes) {
    Write-Host "No production frontend or backend changes to deploy."
    exit 0
}
Write-Host ""
Write-Host "Files that will be deployed:"
Write-Host "----------------------------------------"
$changes | ForEach-Object {
    Write-Host $_
}
Write-Host "----------------------------------------"
Write-Host ""
$answer = Read-Host "Deploy these files? (Y/N)"
if ($answer -notmatch "^[Yy]$") {
    Write-Host "Deploy cancelled. No commit or push was made."
    exit 0
}
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
git commit -m "Online update: $timestamp"
git push origin main
Write-Host ""
Write-Host "========================================"
Write-Host "ONLINE DEPLOY PUSHED SUCCESSFULLY"
Write-Host "Render will deploy the new version."
Write-Host "========================================"
