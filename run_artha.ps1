# Start ARTHA AI backend and frontend (from repo root)
$ErrorActionPreference = "Stop"
$Root = $PSScriptRoot

Write-Host "Starting ARTHA AI..." -ForegroundColor Cyan

# Backend
$backend = Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "Set-Location '$Root\artha_backend'; pip install -r requirements.txt -q; uvicorn main:app --reload --port 8000"
) -PassThru

# Frontend
$frontend = Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "Set-Location '$Root\artha_frontend'; npm run dev"
) -PassThru

Write-Host ""
Write-Host "Backend:  http://localhost:8000  (PID $($backend.Id))" -ForegroundColor Green
Write-Host "Frontend: http://localhost:3000  (PID $($frontend.Id))" -ForegroundColor Green
Write-Host "Auth:     Authorization: Bearer demo-token" -ForegroundColor Yellow
if (-not $env:GEMINI_API_KEY) {
    Write-Host "Warning:  GEMINI_API_KEY not set — AI will use keyword fallback only" -ForegroundColor DarkYellow
} else {
    $model = if ($env:GEMINI_MODEL) { $env:GEMINI_MODEL } else { "gemini-2.0-flash" }
    Write-Host "AI:       Google Gemini ($model)" -ForegroundColor Green
}
Write-Host ""
Write-Host "Close the two PowerShell windows to stop the servers." -ForegroundColor DarkGray
