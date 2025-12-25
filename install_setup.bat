@echo off
setlocal
title MusicSoundLevelUP - One-Click Installer

echo ======================================================
echo   MusicSoundLevelUP Standalone Setup Installer
echo ======================================================
echo.

:: 1. 가상환경 생성
if not exist "venv" (
    echo [1/3] 가상환경(venv) 생성 중...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Python이 설치되어 있지 않거나 경로 설정이 잘못되었습니다.
        pause
        exit /b %errorlevel%
    )
) else (
    echo [SKIP] 가상환경이 이미 존재합니다.
)

:: 2. 라이브러리 설치
echo [2/3] 필수 라이브러리 및 GPU 드라이버(CUDA 11.8) 설치 중...
call .\venv\Scripts\activate
python -m pip install --upgrade pip

:: GPU용 PyTorch 설치 (CUDA 11.8 기준)
echo [Torch] PyTorch GPU 버전을 설치합니다 (시간이 걸릴 수 있습니다)...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

:: 기타 요구사항 설치
echo [Requirements] 기타 라이브러리를 설치합니다...
pip install -r requirements.txt

:: 3. 초기 폴더 생성
echo [3/3] 기본 폴더 구조 생성 중...
if not exist "output" mkdir output
if not exist "training_data" mkdir training_data
if not exist "models" mkdir models

echo.
echo ======================================================
echo   설치가 완료되었습니다! 
echo   'start_station.bat' 파일을 실행하여 앱을 시작하세요.
echo ======================================================
pause
endlocal
