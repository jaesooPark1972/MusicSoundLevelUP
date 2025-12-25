# 🎵 Next-Gen AI Audio Workstation (Colab Edition)

**Created by Music Revolutionary JAESOO**

Google Colab 환경에서 나만의 AI 목소리를 훈련하고, 변환하고, 믹싱까지 할 수 있는 올인원 오디오 워크스테이션입니다. 강력한 GPU를 무료로 활용하여 고품질의 AI 오디오 작업을 수행해보세요.

---

## 🚀 빠른 시작 가이드 (Quick Start)

### 1단계: 준비하기
1. 이 `colab_setup` 폴더 전체를 **구글 드라이브(Google Drive)**에 업로드합니다.
   - 예: `내 드라이브/music_ai/colab_setup`
2. **`Run_on_Colab.ipynb`** 파일을 더블 클릭하여 구글 코랩에서 엽니다.

### 2단계: 환경 설정
1. 상단 메뉴에서 **[런타임]** > **[런타임 유형 변경]**을 클릭합니다.
2. **하드웨어 가속기**를 반드시 **GPU**로 설정하고 저장합니다. (T4 GPU 권장)
3. 노트북의 **1번 셀부터 4번 셀까지 순서대로 실행**하여 필수 라이브러리를 설치하고 환경을 구축합니다.

### 3단계: 앱 실행
1. **5번 셀 (!python colab_app.py)**을 실행합니다.
2. 잠시 후 하단에 생성되는 **`Running on public URL: https://xxxx.gradio.live`** 링크를 클릭하여 웹 UI에 접속합니다.

---

## 🛠️ 주요 기능 사용법

### 1. 🎙️ Voice Training (나만의 목소리 만들기)
실제 사람의 목소리를 학습하여 AI 모델 파일(`.pth`)을 생성합니다.

*   **데이터 준비**: 10초~15분 분량의 깨끗한 목소리 파일들(`.wav`)을 하나의 폴더에 넣고 **ZIP 파일**로 압축하세요.
*   **사용법**:
    1. `Upload Training Data`에 ZIP 파일을 올립니다.
    2. `1. Unzip Data` 버튼을 눌러 압축을 풉니다.
    3. `Model Name`을 입력하고 `Epochs` (학습 반복 횟수)를 설정합니다. (권장: 20~100)
    4. `2. Start Training`을 눌러 학습을 시작합니다.
    5. 완료되면 `.pth` 모델 파일이 생성되어 다운로드할 수 있습니다.

### 2. 🔄 RVC Conversion (목소리 변환)
내 목소리나 다른 가수의 목소리를 학습된 AI 모델의 목소리로 변환합니다.

*   **사용법**:
    1. `Input Vocal File`에 변환할 원본 목소리 파일(WAV/MP3)을 올립니다.
    2. `Upload .pth Model`에 학습된 모델 파일을 올립니다.
    3. `Convert Voice` 버튼을 누르면 변환된 오디오가 생성됩니다.

### 3. 🎛️ AI Studio Mixing (믹싱 및 마스터링)
보컬과 반주(MR)를 전문가 수준으로 합치고, 음질을 향상시킵니다.

*   **기능**:
    *   **AI Enhancement**: 노이즈 제거, 이퀄라이저, 컴프레서 자동 적용
    *   **Pro Effects**: Dolby 스타일 효과, Hi-Fi 모드 지원
    *   **RVC 연동**: 믹싱 전 자동으로 목소리 변환 가능
*   **사용법**:
    1. `Vocal Track`과 `MR / Instrumental` 파일을 각각 업로드합니다.
    2. 볼륨 밸런스와 리버브(잔향) 양을 조절합니다.
    3. (선택) `Enable RVC Conversion`을 체크하고 모델을 올리면, 보컬을 AI 목소리로 바꾼 뒤 믹싱합니다.
    4. `Start AI Mixing` 버튼을 누르세요.

---

## ⚠️ 문제 해결 (Troubleshooting)

**Q. "str object has no attribute 'name'" 에러가 떠요.**
*   최신 Gradio 업데이트로 인한 문제위였으나, **현재 코드(v2.1)에서는 이미 수정되었습니다.**
*   만약 이 에러가 보인다면, `colab_app.py`가 최신 버전인지 확인하고 코랩의 **5번 셀**을 정지 후 재실행해주세요.

**Q. 변환된 목소리가 기계음 같아요.**
*   **학습 데이터 부족**: 더 많은 녹음 데이터(최소 10분 이상)로 다시 학습해보세요.
*   **과적합(Overfitting)**: Epoch를 너무 높게 잡으면 발생할 수 있습니다. Epoch를 조금 낮춰보세요.

**Q. 파일 업로드가 안 돼요.**
*   브라우저의 인터넷 연결을 확인하거나, Gradio 페이지를 새로고침(F5) 해보세요. 코랩 런타임이 끊겼다면 다시 연결해야 합니다.

---

**Version**: 2.1 (Colab Optimized)
**Author**: Park Jae-soo (SKY Group)
