# PowerShell 실행 스크립트
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  Next-Gen AI Audio Workstation - GUI Version (HQ)" -ForegroundColor Yellow
Write-Host "  Starting Application..." -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

# 가상환경 활성화
& "$scriptDir\venv\Scripts\Activate.ps1"

# Python 프로그램 실행
python "$scriptDir\ai_audio_studio_pro.py"

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[ERROR] The program crashed!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
}
