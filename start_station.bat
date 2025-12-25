@echo off
:: 한글 인코딩 설정 및 현재 경로(D드라이브) 강제 고정
chcp 65001 > nul
setlocal
cd /d "%~dp0"

:: [경로 설정] 부모 폴더 및 현재 폴더의 venv 경로 정의
set "PARENT_VENV_PATH=..\venv\Scripts\activate.bat"
set "CURRENT_VENV_PATH=.\venv\Scripts\activate.bat"

:main_menu
cls
echo ======================================================
echo    MusicSoundLevelUP 통합 워크스테이션 (CUDA 연동)
echo ======================================================
echo  현재 위치: %cd%
echo ======================================================
echo  1. [실행] AI 워크스테이션 시작 (로컬 GPU 사용)
echo  2. [실행] 오버나이트 배치 (1,200컷 자동화)
echo  3. [설치/수리] 환경 체크 및 라이브러리 강제 설치
echo  4. [도움말] 구글 코랩(Colab) 가이드 보기
echo  5. 프로그램 종료
echo ======================================================
set /p choice="번호를 입력하세요 (1-5): "

if "%choice%"=="1" goto check_env
if "%choice%"=="2" goto run_batch
if "%choice%"=="3" goto install_env
if "%choice%"=="4" goto run_colab
if "%choice%"=="5" exit
goto main_menu

:check_env
cls
echo [정보] 시스템 환경을 분석 중입니다...
:: 1순위: 부모 폴더 venv 확인
if exist "%PARENT_VENV_PATH%" (
    echo [확인] 부모 폴더의 venv를 발견했습니다. 연동합니다.
    call "%PARENT_VENV_PATH%"
    goto start_app
)
:: 2순위: 현재 폴더 venv 확인
if exist "%CURRENT_VENV_PATH%" (
    echo [확인] 현재 폴더의 venv를 사용합니다.
    call "%CURRENT_VENV_PATH%"
    goto start_app
)
:: venv가 없을 경우
echo [알림] venv를 찾을 수 없어 새로 설치 메뉴로 이동합니다.
pause
goto install_env

:start_app
cls
echo [정보] GPU 및 CUDA 환경을 체크합니다...
:: Python을 통해 CUDA 사용 가능 여부 출력 (사용자 피드백용)
python -c "import torch; print('✓ GPU(CUDA) 인식 성공' if torch.cuda.is_available() else '⚠️ GPU 인식 실패 (CPU 모드로 실행)')"
echo [진행] 앱을 실행합니다. 잠시만 기다려 주세요...
python colab_app.py
pause
goto main_menu

:install_env
cls
echo [설치] 설치된 Python과 CUDA를 찾아 라이브러리를 구성합니다.
if not exist "venv" (
    echo [진행] venv 가상환경 생성 중...
    python -m venv venv
)
call .\venv\Scripts\activate
echo [진행] CUDA 전용 PyTorch 및 필수 패키지 설치 중...
pip install --upgrade pip
pip install -r requirements.txt
:: 사용자의 CUDA 환경에 맞춘 PyTorch 설치 (NVIDIA GPU 최적화)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install torchcodec faiss-cpu librosa
echo [완료] 모든 라이브러리 구성이 완료되었습니다!
pause
goto main_menu

:run_batch
cls
echo [정보] 1,200컷 오버나이트 배치 모드 가동... [cite: 2025-12-12]
call "%PARENT_VENV_PATH%" 2>nul || call "%CURRENT_VENV_PATH%"
python colab_app.py --batch
pause
goto main_menu

:run_colab
start https://colab.research.google.com/
goto main_menu