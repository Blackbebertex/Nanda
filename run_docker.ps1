# Start ARTHA AI with Docker Compose
Set-Location $PSScriptRoot

if (-not (Test-Path ".env")) {
  Write-Host "Create .env from .env.example and set GEMINI_API_KEY first." -ForegroundColor Yellow
  exit 1
}

docker compose up --build -d
Write-Host ""
Write-Host "ARTHA AI is running:" -ForegroundColor Green
Write-Host "  App:  http://localhost:3000"
Write-Host "  API:  http://localhost:8000/health"
Write-Host ""
Write-Host "Stop: docker compose down"
