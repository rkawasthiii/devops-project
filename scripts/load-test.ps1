# Load generator for the HPA demo (PowerShell).
#
#   .\scripts\load-test.ps1 -BaseUrl http://localhost:8000 -DurationSeconds 120
# Then watch: kubectl get hpa -n medidesk -w

param(
    [string]$BaseUrl = "http://localhost:8000",
    [int]$DurationSeconds = 120
)

Write-Host "Load-testing $BaseUrl for ${DurationSeconds}s — watch 'kubectl get hpa'"
$deadline = (Get-Date).AddSeconds($DurationSeconds)
$ok = 0
$fail = 0

while ((Get-Date) -lt $deadline) {
    foreach ($path in "/api/appointments", "/api/appointments/stats") {
        try {
            Invoke-WebRequest -Uri "$BaseUrl$path" -UseBasicParsing -TimeoutSec 5 | Out-Null
            $ok++
        } catch {
            $fail++
        }
    }
}

Write-Host "done: $ok requests ok, $fail failed"
