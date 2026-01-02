@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo ========================================================
echo 🚀 Next-Gen AI Audio Workstation - Portable Setup
echo ========================================================
echo.

:: 1. Python Check
echo [1/7] Checking Python Environment...
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found!
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    echo IMPOTANT: Check "Add Python to PATH" during installation.
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo    - Python %PYTHON_VERSION% detectd.

:: 2. VC++ Check (Simple)
reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64" /v "Version" >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [WARNING] Visual C++ Redistributable might be missing.
    echo If you see "DLL load failed" later, install it from:
    echo https://aka.ms/vs/17/release/vc_redist.x64.exe
) else (
    echo    - VC++ Redistributable detected.
)
echo.

:: 3. Create Virtual Environment
echo [2/7] Setting up Virtual Environment...
if not exist "venv" (
    echo    - Creating venv...
    python -m venv venv
    if !errorlevel! neq 0 (
        echo [ERROR] Failed to create venv.
        pause
        exit /b 1
    )
) else (
    echo    - Using existing venv.
)

:: 4. Upgrade PIP
echo [3/7] Upgrading PIP...
call venv\Scripts\python.exe -m pip install --upgrade pip --quiet
echo    - PIP upgraded.
echo.

:: 5. Install PyTorch (CUDA 12.1)
echo [4/7] Installing PyTorch (CUDA 12.1)...
echo    - This may take a while...
call venv\Scripts\pip.exe install torch torchaudio --index-url https://download.pytorch.org/whl/cu121 --quiet --no-warn-script-location
if %errorlevel% neq 0 (
    echo [WARNING] Standard PyTorch installation failed. Retrying...
    call venv\Scripts\pip.exe install torch torchaudio
)
echo    - PyTorch installed.
echo.

:: 6. Install Requirements
echo [5/7] Installing AI Core Dependencies...
:: Install core scientific packages first to avoid build issues
call venv\Scripts\pip.exe install numpy==1.26.4 pandas==2.1.4 --quiet --no-warn-script-location

:: Install other requirements
call venv\Scripts\pip.exe install customtkinter requests pydub librosa demucs soundfile music21 Pillow mir_eval onnxruntime scipy --quiet --no-warn-script-location
call venv\Scripts\pip.exe install gradio tensorflow tf-keras --quiet --no-warn-script-location

:: Basic pitch (optional, might fail due to conflicts, so we suppress error)
call venv\Scripts\pip.exe install basic-pitch --quiet --no-warn-script-location >nul 2>&1

echo    - Core dependencies installed.
echo.

:: 7. Create Directories
echo [6/7] Creating Folder Structure...
if not exist "ffmpeg" mkdir ffmpeg
if not exist "output_result" mkdir output_result
if not exist "models\checkpoints" mkdir "models\checkpoints"
if not exist "assets\hubert" mkdir "assets\hubert"
if not exist "assets\pretrained_v2" mkdir "assets\pretrained_v2"
if not exist "temp_work" mkdir temp_work
echo    - Folders created.

:: 8. External Tools (FFmpeg & LilyPond)
echo [7/7] Checking External Tools...

:: FFmpeg Check
if not exist "ffmpeg\ffmpeg.exe" (
    echo    - FFmpeg not found in 'ffmpeg' folder.
    echo    - Attempting auto-download...
    powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip' -OutFile 'ffmpeg.zip'}"
    
    if exist "ffmpeg.zip" (
        powershell -Command "Expand-Archive -Path 'ffmpeg.zip' -DestinationPath 'ffmpeg_temp' -Force"
        for /r "ffmpeg_temp" %%f in (ffmpeg.exe ffprobe.exe) do (
            copy "%%f" "ffmpeg\" > nul
        )
        rd /s /q ffmpeg_temp
        del ffmpeg.zip
        echo    - FFmpeg downloaded and installed.
    ) else (
        echo    [WARNING] FFmpeg download failed. Please install manually.
    )
) else (
    echo    - FFmpeg detected.
)

:: LilyPond Check
if not exist "lilypond-2.24.4" (
    if not exist "C:\lilypond-2.24.4" (
        echo    [INFO] LilyPond not found (Local or C:\). 
        echo    - Attempting auto-download...
        powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://gitlab.com/lilypond/lilypond/-/releases/v2.24.4/downloads/lilypond-2.24.4-mingw-x86_64.zip' -OutFile 'lilypond.zip'}"
        
        if exist "lilypond.zip" (
            powershell -Command "Expand-Archive -Path 'lilypond.zip' -DestinationPath '.' -Force"
            del lilypond.zip
            echo    - LilyPond downloaded and installed.
            set "LILY_PATH=%~dp0lilypond-2.24.4\bin"
        ) else (
             echo    [WARNING] LilyPond download failed.
             set "LILY_PATH="
        )
    ) else (
        echo    - LilyPond detected at C:\lilypond-2.24.4
        set "LILY_PATH=C:\lilypond-2.24.4\bin"
    )
) else (
    echo    - LilyPond detected in local folder.
    set "LILY_PATH=%~dp0lilypond-2.24.4\bin"
)

:: 9. MuseScore Check & Config Generation
echo [8/7] Linking Paths & Generating Config...

set "MS_PATH="
if exist "C:\Program Files\MuseScore 4\bin\MuseScore4.exe" (
    set "MS_PATH=C:\Program Files\MuseScore 4\bin"
    echo    - MuseScore 4 detected.
) else (
    if exist "C:\Program Files\MuseScore 3\bin\MuseScore3.exe" (
        set "MS_PATH=C:\Program Files\MuseScore 3\bin"
        echo    - MuseScore 3 detected.
    ) else (
        echo    [WARNING] MuseScore not found in default paths.
    )
)

:: Generate config.json using Python
echo    - Generating config.json...
(
echo import json
echo import os
echo import sys
echo config = {}
echo config['python_venv_path'] = os.path.abspath('venv')
echo config['lilypond_path'] = r'%LILY_PATH%'
echo config['musescore_path'] = r'%MS_PATH%'
echo config['system_python_path'] = sys.executable
echo with open('config.json', 'w', encoding='utf-8') as f:
echo     json.dump(config, f, indent=4, ensure_ascii=False)
) > create_config.py

venv\Scripts\python.exe create_config.py
del create_config.py
echo    - Configuration linked successfully.

echo.
echo ========================================================
echo 🎉 Setup Complete!
echo ========================================================
echo.
echo You can now run 'run_gui.bat' to start the application.
echo.
pause
