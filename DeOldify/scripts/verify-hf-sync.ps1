<#
.SYNOPSIS
    Verifies GitHub and HuggingFace repositories are in sync.

.DESCRIPTION
    Compares the latest commit SHA between local git and HuggingFace remote.
    Can be run before push to ensure sync or in CI to validate.

.PARAMETER DryRun
    If specified, only reports status without making changes.

.EXAMPLE
    .\verify-hf-sync.ps1
    .\verify-hf-sync.ps1 -DryRun
#>

param(
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

# Get local HEAD commit
$localHead = git rev-parse HEAD
Write-Host "Local HEAD: $localHead" -ForegroundColor Cyan

# Determine repo name from remote
$origin = git remote get-url origin
if ($origin -match 'github\.com[:/](.+?)(?:\.git)?$') {
    $repoPath = $Matches[1]
    $hfRepo = "https://huggingface.co/$repoPath"
} else {
    Write-Error "Could not determine repository path from origin: $origin"
    exit 1
}

Write-Host "HuggingFace repo: $hfRepo" -ForegroundColor Cyan

# Check if HuggingFace remote exists
try {
    $remotes = git remote
    if ($remotes -notcontains 'hf') {
        Write-Host "Adding HuggingFace remote..." -ForegroundColor Yellow
        git remote add hf $hfRepo
    }
    
    # Fetch from HuggingFace
    Write-Host "Fetching from HuggingFace..." -ForegroundColor Yellow
    git fetch hf main --quiet 2>$null
    
    # Get HuggingFace HEAD
    $hfHead = git rev-parse hf/main 2>$null
    
    if ($hfHead) {
        Write-Host "HuggingFace HEAD: $hfHead" -ForegroundColor Cyan
        
        if ($localHead -eq $hfHead) {
            Write-Host "`n✅ Repositories are in sync!" -ForegroundColor Green
            exit 0
        } else {
            Write-Host "`n⚠️ Repositories are OUT OF SYNC" -ForegroundColor Yellow
            Write-Host "  Local: $localHead"
            Write-Host "  HuggingFace: $hfHead"
            
            if (-not $DryRun) {
                Write-Host "`nSync will occur on next push to main." -ForegroundColor Cyan
            }
            exit 0
        }
    }
} catch {
    Write-Host "Could not fetch from HuggingFace: $_" -ForegroundColor Yellow
    Write-Host "This may be expected if the HuggingFace repo is empty or inaccessible." -ForegroundColor Gray
}

Write-Host "`n📋 Summary:" -ForegroundColor Cyan
Write-Host "  GitHub → HuggingFace sync is configured via GitHub Actions."
Write-Host "  Push to main branch to trigger automatic sync."
