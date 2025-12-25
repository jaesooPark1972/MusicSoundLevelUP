import gradio as gr
import os
import sys

# [중요] 상대 경로 설정 - 로컬/코랩 자동 대응
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
MODELS_DIR = os.path.join(BASE_DIR, "models")

for d in [OUTPUT_DIR, MODELS_DIR]:
    os.makedirs(d, exist_ok=True)

# 디자인: 유니콘 스튜디오 120% 확대 (로고 가리기)
unicorn_html = """
<div style="width: 100%; height: 350px; overflow: hidden; border-radius: 20px; position: relative; background: #000;">
    <div data-us-project="5OOi62lpBTZdxkeZW75n" 
         style="width: 120%; height: 120%; position: absolute; top: -15%; left: -10%;">
    </div>
</div>
<script type="text/javascript">!function(){if(!window.UnicornStudio){window.UnicornStudio={isInitialized:!1};var i=document.createElement("script");i.src="https://cdn.jsdelivr.net/gh/hiunicornstudio/unicornstudio.js@v1.5.3/dist/unicornStudio.umd.js",i.onload=function(){window.UnicornStudio.isInitialized||(UnicornStudio.init(),window.UnicornStudio.isInitialized=!0)},(document.head || document.body).appendChild(i)}}();</script>
"""

# colab_app.py 70~80행 부근 (RVC Conversion 부분)
def run_rvc_conversion(vocal_file, model_file):
    if not vocal_file or not model_file:
        return "파일이 부족합니다.", None
    try:
        # [.name 제거] Gradio 4.x 이상의 문자열 경로 방식을 완벽 지원합니다.
        success = converter.load_model(model_file) 
        output_name = f"result_{int(time.time())}.wav"
        output_path = os.path.join(OUTPUT_DIR, output_name)
        
        if converter.convert(vocal_file, output_path):
            return "AI 목소리 변환 완료!", output_path
        return "변환 중 오류 발생", None
    except Exception as e:
        return f"에러 로그: {str(e)}", None

# (이하 Gradio Blocks 레이아웃...)