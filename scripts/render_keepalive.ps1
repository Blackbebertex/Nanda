# Ping Render API every 50s to reduce free-tier cold starts during demos.
param(
  [string]$ApiUrl = $env:RENDER_API_URL,
  [int]$IntervalSeconds = 50
)

if (-not $ApiUrl) {
  $ApiUrl = "https://artha-api-lsli.onrender.com"
}

$PingUrl = ($ApiUrl.TrimEnd("/")) + "/v1/demo/hello"
Write-Host "ARTHA keep-alive -> $PingUrl every ${IntervalSeconds}s (Ctrl+C to stop)"

while ($true) {
  try {
    $r = Invoke-RestMethod -Uri $PingUrl -TimeoutSec 30
    Write-Host "$(Get-Date -Format 'HH:mm:ss') hello -> $($r.message) [$($r.status)]"
  } catch {
    Write-Host "$(Get-Date -Format 'HH:mm:ss') ping failed: $_" -ForegroundColor Yellow
  }
  Start-Sleep -Seconds $IntervalSeconds
}
