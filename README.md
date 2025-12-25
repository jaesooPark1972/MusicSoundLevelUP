# 🎵 Next-Gen AI Audio Workstation (Colab Edition)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jaesooPark1972/MusicSoundLevelUP/blob/main/Run_on_Colab.ipynb)
![GitHub repo size](https://img.shields.io/github/repo-size/jaesooPark1972/MusicSoundLevelUP)
![License](https://img.shields.io/badge/license-MIT-blue)

**Created by Music Revolutionary JAESOO**

GitHub와 Google Colab의 강력한 연동을 통해, 설치 없이 원클릭으로 실행하는 **올인원 AI 오디오 워크스테이션**입니다. 200페이지 분량의 대규모 오디오 작업을 위한 로컬 환경 최적화 설정도 지원합니다.

---

## 🚀 바로 시작하기 (One-Click Start)

### 가장 쉬운 방법 (권장)
위의 **`Open In Colab`** 배지를 클릭하면 즉시 실행됩니다!

1. **배지 클릭**: 페이지 상단의 `Open In Colab` 버튼을 누릅니다.
2. **GPU 설정**: 열린 코랩 화면에서 상단 메뉴 `런타임` > `런타임 유형 변경` > **GPU** 선택 후 저장.
3. **전체 실행**: `Ctrl + F9` 또는 메뉴의 `런타임` > `모두 실행`을 누르면 끝!
4. 잠시 후 맨 아래 셀에 나오는 **`gradio.live` 링크**를 클릭하여 접속하세요.

---

## 💻 로컬 PC 환경 구축 (Local Standalone)

대규모 작업(1,200개 컷 등)이나 끊김 없는 훈련을 위해 권장되는 설정입니다.

### 1. 하드웨어 가속 설정 (GPU 필수)
로컬 PC에서 GPU를 인식시키기 위해 다음 설치가 필요합니다.
*   **NVIDIA 드라이버**: 최신 그래픽 카드 드라이버 설치
*   **CUDA Toolkit**: 11.8 또는 12.1 버전 권장
*   **PyTorch (GPU용)**: `install_setup.bat` 실행 시 자동으로 설치됩니다. (CUDA 11.8 기반)

### 2. 원클릭 설치 및 실행
1. 이 프로젝트를 다운로드하거나 Clone 합니다.
2. **`install_setup.bat`** 실행: 가상환경(`venv`) 생성 및 라이브러리 자동 설치.
3. **`start_station.bat`** 실행:
    *   **일반 모드**: Gradio 웹 UI를 띄워 작업합니다.
    *   **배치 모드 (Overnight Batch)**: 대규모 작업을 위해 에러 발생 시 자동 재시작 및 루프(1시간 간격) 기능을 지원합니다.

### 3. 배포 패키지 제작
*   **`build_exe.bat`** 파일을 실행하면 외부 노출 없이 실행 가능한 `.exe` 파일이 `dist/` 폴더에 생성됩니다.

---

## 📁 프로젝트 구조 (Folder Structure)

```text
MusicSoundLevelUP/
├── venv/                # 가상환경 (자동 생성)
├── models/              # AI 음성 모델 파일 저장소
├── training_data/       # 학습용 오디오 데이터 ZIP/WAV
├── output/              # 변환 및 믹싱 결과물 저장
├── colab_app.py         # 메인 실행 코드 (CLI/UI 지원)
├── rvc_trainer.py       # RVC 변환 엔진
├── voice_trainer.py     # 목소리 훈련 엔진
├── install_setup.bat    # 원클릭 환경 구축
├── start_station.bat    # 원클릭 앱 실행 (일반/배치 선택)
└── build_exe.bat        # EXE 배포 파일 제작 도구
```

---

## 🛠️ 주요 기능

### 1. 🎙️ Voice Training (나만의 목소리 만들기)
*   **학습**: RVC 기반의 고성능 엔진으로 나만의 `.pth` 모델 생성
*   **최적화**: VRAM 3GB (GTX 1060 등) 환경에서도 끊김 없는 훈련 지원

### 2. 🔄 RVC Conversion (목소리 변환)
*   **변환**: 내 목소리를 학습된 모델의 목소리로 고품질 변환
*   **Batch**: 수백 개의 파일을 한 번에 처리하는 배치 시스템 지원

### 3. 🎛️ AI Studio Mixing (프로 믹싱)
*   **효과**: 노이즈 제거, 리버브, Dolby Style, Hi-Fi 모드 지원
*   **디자인**: Unicorn Studio 커스텀 스크립트 적용으로 시각적으로 화려하고 세련된 UI 제공 (로고 가림 트릭 적용)

### 4. 🚀 Massive Batch Processing (대규모 자동화)
*   **대상**: 200페이지 분량, 1,200개 이상의 오디오 컷 작업에 특화
*   **방식**: `batch_input` 폴더에 파일을 넣고 '배치 모드'로 실행하면 자동으로 전 파일을 순회하며 변환
*   **추천**: `page_001_cut_01.wav`와 같은 명명 규칙 사용 시 결과물 관리가 더욱 용이합니다.

---

## ⚠️ FAQ

**Q. "str object has no attribute 'name'" 에러가 떠요.**
*   최신 Gradio 업데이트에 대응하여 수정 완료되었습니다. `start_station.bat`을 재실행하거나 코룸의 5번 셀을 재실행하세요.

**Q. 훈련 속도가 너무 느려요.**
*   반드시 NVIDIA GPU 환경인지 확인하세요. (AMD 그래픽카드는 공식 지원되지 않습니다.)

---

**Repository**: [jaesooPark1972/MusicSoundLevelUP](https://github.com/jaesooPark1972/MusicSoundLevelUP)
**Version**: 2.2 (Local & Cloud Hybrid)
**Author**: Park Jae-soo (SKY Group)
