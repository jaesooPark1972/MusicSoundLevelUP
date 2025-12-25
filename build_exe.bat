@echo off
setlocal
title MusicSoundLevelUP - EXE Builder

echo ======================================================
echo   MusicSoundLevelUP EXE Packaging (PyInstaller)
echo ======================================================
echo.

call .\venv\Scripts\activate

:: PyInstaller 설치 확인
echo [1/2] PyInstaller 설치 확인 중...
pip install pyinstaller

:: 빌드 실행
echo [2/2] EXE 빌드를 시작합니다 (dist 폴더 확인)...
pyinstaller --noconfirm --onedir --windowed ^
    --add-data "models;models" ^
    --add-data "training_data;training_data" ^
    --icon=NONE ^
    colab_app.py

echo.
echo ======================================================
echo   빌드 완료! 'dist/colab_app' 폴더를 확인하세요.
echo ======================================================
pause
endlocal
