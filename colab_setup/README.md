# 🎵 MusicSoundLevelUP (Bento Edition v2.4)

### Next-Gen AI Audio Workstation (Massive + Bento Style)

**Created by Music Revolutionary JAESOO (SKY Group)**

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jaesooPark1972/MusicSoundLevelUP/blob/main/colab_setup/Run_on_Colab.ipynb)

본 프로젝트는 200페이지 분량, 1,200개 이상의 대규모 오디오 작업을 위해 설계된 전문가용 AI 워크스테이션입니다. **Bento Grid** 스타일이 적용된 최신 다크 테마 UI를 제공하며, 드라이브 경로에 상관없이 로컬 PC와 구글 코랩(Colab) 환경을 모두 지원합니다.

---

## 🎨 주요 디자인 변경 사항 (v2.4 Bento Edition)

* **Bento Grid Layout**: 모든 기능을 카드 형태의 직관적인 레이아웃으로 재구성하여 사용성을 극대화했습니다.
* **Deep Dark Theme**: `Zinc 950` 기반의 고급스러운 다크 테마를 적용하여 눈의 피로를 줄이고 몰입감을 높였습니다.
* **Solar Icons**: 모든 텍스트 버튼을 직관적인 Solar Icon Sets으로 교체하여 심미성을 강화했습니다.
* **Unicorn Studio Integration**: 상단에 120% 확대된(로고 숨김) 화려한 인터랙티브 백그라운드를 적용했습니다.

---

## 🚀 바로 시작하기 (One-Click Start)

### 1. Cloud 환경 (Google Colab)

위의 배지를 클릭하여 노트북을 열고 **GPU 런타임**에서 실행하세요. 자동으로 최신 디자인이 적용된 웹 UI가 실행됩니다.

* **Tip**: 실행 후 나타나는 `public URL`을 클릭하면 전체 화면으로 즐길 수 있습니다.

### 2. Local PC 환경 (Windows)

* `start_station.bat` 또는 `run_gui.bat`를 실행하면 자동으로 가상환경을 잡고 실행됩니다.
* **GPU 가속**: NVIDIA CUDA 자동 감지 및 가속 지원.

---

## 💻 설치 및 실행 가이드

### STEP 1. 환경 구축

1. `start_station.bat` 실행 -> **2번(설치/수리)** 선택.
2. Python, CUDA, venv 자동 구성.

### STEP 2. 앱 실행

1. `start_station.bat` 실행 -> **1번(실행)** 선택.
2. Gradio 웹 UI 자동 실행.

---

## 📁 프로젝트 구조

```text
MusicSoundLevelUP/
├── venv/                 # [자동탐색] 상위 또는 현재 폴더의 가상환경
└── colab_setup/          # 작업 메인 폴더
    ├── colab_app.py      # 메인 코드 (Bento Grid UI 적용)
    ├── start_station.bat # 통합 실행기
    ├── models/           # AI 음성 모델(.pth)
    ├── output/           # 결과물 저장소
    └── requirements.txt  # 필수 라이브러리
```

---

## ⚠️ FAQ

**Q: GitHub Push 시 권한 오류가 발생합니다.**

* SSH Key가 올바르게 등록되어 있는지 확인하세요. 오류가 지속되면 HTTPS 방식으로 다시 시도하거나, SSH 에이전트에 키를 등록해야 합니다.

---

**Repository**: [jaesooPark1972/MusicSoundLevelUP](https://github.com/jaesooPark1972/MusicSoundLevelUP)
**Author**: Park Jae-soo (SKY Group)
**Version**: 2.4 (Bento Edition)
