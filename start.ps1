# Start NutriAI — AI Nutrition Assistant
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host " NutriAI — AI Nutrition Assistant" -ForegroundColor Cyan
Write-Host " Powered by IBM Granite (watsonx.ai)" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Check for .env file
if (-not (Test-Path ".env")) {
    Write-Host ""
    Write-Host "[WARN] No .env file found. Creating from template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "[ACTION] Please edit .env with your IBM Cloud credentials before continuing." -ForegroundColor Yellow
    Write-Host "         Required: WATSONX_API_KEY and WATSONX_PROJECT_ID" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter after editing .env to continue"
}

# Install dependencies
Write-Host ""
Write-Host "[1/2] Installing Python dependencies..." -ForegroundColor Green
pip install -r requirements.txt --quiet

# Start server
Write-Host ""
Write-Host "[2/2] Starting NutriAI server..." -ForegroundColor Green
Write-Host ""
Write-Host "  Open http://localhost:8000 in your browser" -ForegroundColor White
Write-Host "  API docs at http://localhost:8000/docs" -ForegroundColor White
Write-Host "  Press Ctrl+C to stop" -ForegroundColor White
Write-Host ""

python main.py
