# CoreMind Platform Startup Script
# This script starts Flowise, ngrok, and updates the config automatically

Write-Host "🚀 Starting CoreMind Platform..." -ForegroundColor Cyan

# Start Flowise in background
Write-Host "📦 Starting Flowise..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "npx flowise start" -WindowStyle Minimized

# Wait for Flowise to start
Write-Host "⏳ Waiting for Flowise to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Start ngrok in background
Write-Host "🌐 Starting ngrok tunnel..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "ngrok http 3000" -WindowStyle Minimized

# Wait for ngrok to start
Write-Host "⏳ Waiting for ngrok to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Get ngrok URL
Write-Host "🔍 Fetching ngrok URL..." -ForegroundColor Yellow
$ngrokUrl = (Invoke-RestMethod -Uri "http://127.0.0.1:4040/api/tunnels").tunnels[0].public_url

if ($ngrokUrl) {
    Write-Host "✅ Ngrok URL: $ngrokUrl" -ForegroundColor Green
    
    # Update config.js
    Write-Host "📝 Updating config.js..." -ForegroundColor Yellow
    $configPath = "platform/config.js"
    $configContent = Get-Content $configPath -Raw
    
    # Replace the URL in config.js
    $newConfig = $configContent -replace "FLOWISE_API_URL: 'https://[^']+/api/v1/prediction/([^']+)'", "FLOWISE_API_URL: '$ngrokUrl/api/v1/prediction/`$1'"
    
    Set-Content -Path $configPath -Value $newConfig
    
    Write-Host "✅ Config updated!" -ForegroundColor Green
    
    # Git commit and push
    Write-Host "📤 Pushing to GitHub..." -ForegroundColor Yellow
    git add platform/config.js
    git commit -m "Auto-update: ngrok URL changed to $ngrokUrl"
    git push
    
    Write-Host "✅ Changes pushed to GitHub!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🎉 Platform is now LIVE!" -ForegroundColor Cyan
    Write-Host "Frontend: https://turyasin.github.io/platform/dashboard.html" -ForegroundColor White
    Write-Host "Backend: $ngrokUrl" -ForegroundColor White
    Write-Host ""
    Write-Host "Press any key to exit..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
} else {
    Write-Host "❌ Failed to get ngrok URL. Please check if ngrok is running." -ForegroundColor Red
}
