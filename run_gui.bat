@echo off
cd /d "%~dp0"

echo ========================================================
echo   Next-Gen AI Audio Workstation - GUI Version (HQ)
echo   Starting Application...
echo ========================================================
echo.

call ".venv\Scripts\activate.bat"

python ai_audio_studio_pro.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] The program crashed!
    pause
)

pause