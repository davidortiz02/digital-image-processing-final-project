# Simple script to serve the DeOldify project root and open the browser
Write-Host "Starting local server for DeOldify Browser..." -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server." -ForegroundColor Yellow

# Get the root directory (parent of the script's directory)
$scriptPath = $MyInvocation.MyCommand.Path
$browserDir = Split-Path $scriptPath
$rootDir = Split-Path $browserDir

# Change to root directory
Set-Location $rootDir
Write-Host "Serving from: $rootDir" -ForegroundColor Gray

# Start the server in the background
$process = Start-Process -FilePath "python" -ArgumentList "-m http.server 8000" -PassThru

# Wait a moment for it to start
Start-Sleep -Seconds 2

# Open the browser to the artistic page
Start-Process "http://localhost:8000/browser/artistic.html"

# Wait for the user to close the script
Read-Host "Server is running. Press Enter to stop server and exit..."

# Stop the server
Stop-Process -Id $process.Id
