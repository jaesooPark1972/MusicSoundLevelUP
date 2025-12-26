import gradio as gr
import os
import shutil
import zipfile
import threading
import time
import argparse
import sys
from voice_trainer import RealVoiceTrainer
from rvc_trainer import VoiceConverter
from vocal_enhancer import VocalEnhancer

# Paths - Automatically detect base directory for local/packaged distribution (v2.3)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
TRAIN_DATA_DIR = os.path.join(BASE_DIR, "training_data")
MODELS_DIR = os.path.join(BASE_DIR, "models")

for d in [OUTPUT_DIR, TRAIN_DATA_DIR, MODELS_DIR]:
    os.makedirs(d, exist_ok=True)

# Global instances
trainer = RealVoiceTrainer()
converter = VoiceConverter()
enhancer = VocalEnhancer()

def get_model_dict(custom_path=None):
    """models 폴더, output_result, 그리고 사용자 커스텀 폴더에서 .pth 파일을 검색하여 {표시이름: 전체경로} 반환"""
    model_dict = {}
    search_dirs = [MODELS_DIR, os.path.join(BASE_DIR, "output_result")]
    if custom_path and os.path.exists(custom_path):
        search_dirs.append(custom_path)
    
    for d in search_dirs:
        if not os.path.exists(d): continue
        for root, dirs, files in os.walk(d):
            for f in files:
                if f.endswith('.pth'):
                    full_path = os.path.join(root, f)
                    # 표시 이름 결정 (파일명에서 .pth 제외)
                    display_name = os.path.splitext(f)[0]
                    # 중복 이름 방지를 위해 폴더명 살짝 추가 (선택사항)
                    parent_dir = os.path.basename(os.path.dirname(full_path))
                    unique_name = f"{display_name} ({parent_dir})"
                    model_dict[unique_name] = full_path
                    
    return model_dict

def get_index_for_model(model_path):
    """모델 파일과 같은 이름의 .index 파일이 있는지 확인"""
    if not model_path: return None
    index_path = model_path.replace('.pth', '.index')
    if os.path.exists(index_path):
        return index_path
    
    # 같은 폴더 내의 다른 .index 파일 검색
    folder = os.path.dirname(model_path)
    if os.path.exists(folder):
        indices = [f for f in os.listdir(folder) if f.endswith('.index')]
        if indices: return os.path.join(folder, indices[0])
        
    return None

def generate_index_manually(model_path, dataset_path, progress=gr.Progress()):
    """이미 학습된 모델에 대해 .index 파일만 수동 생성"""
    if not model_path or not dataset_path:
        return "모델과 데이터셋 경로를 모두 확인해주세요."
    
    try:
        progress(0.1, desc="Initializing Index Generator...")
        model_name = os.path.splitext(os.path.basename(model_path))[0]
        
        # trainer의 로직을 빌려와서 인덱스만 생성
        save_dir = os.path.dirname(model_path)
        
        progress(0.3, desc="Extracting Features from dataset...")
        # trainer의 인스턴스를 사용하여 특징 추출
        trainer.feature_buffer = []
        
        # 데이터셋 폴더 내 오디오 스캔
        audio_files = []
        for root, dirs, files in os.walk(dataset_path):
            for f in files:
                if f.endswith(('.wav', '.flac', '.mp3')):
                    audio_files.append(os.path.join(root, f))
        
        if not audio_files:
            return "오디오 파일을 찾을 수 없습니다."
            
        import torchaudio
        import faiss
        import numpy as np
        
        for i, audio_file in enumerate(audio_files):
            progress(0.3 + (i/len(audio_files)*0.5), desc=f"Processing {os.path.basename(audio_file)}...")
            try:
                wav, sr = torchaudio.load(audio_file)
                if sr != 16000:
                    resampler = torchaudio.transforms.Resample(sr, 16000)
                    wav = resampler(wav)
                
                if wav.shape[0] > 1: wav = wav.mean(0, keepdim=True)
                
                mel = trainer.extract_mel_spectrogram(wav)
                feat = mel.squeeze(0).transpose(0, 1).cpu().numpy()
                trainer.feature_buffer.append(feat)
            except: continue
            
        if not trainer.feature_buffer:
            return "특징 추출에 실패했습니다."
            
        progress(0.9, desc="Building FAISS Index...")
        all_features = np.concatenate(trainer.feature_buffer, axis=0).astype('float32')
        index = faiss.IndexFlatL2(80)
        index.add(all_features)
        
        index_path = os.path.join(save_dir, f"{model_name}.index")
        faiss.write_index(index, index_path)
        trainer.feature_buffer = []
        
        return f"✅ 성공! 인덱스 생성 완료: {index_path}"
    except Exception as e:
        return f"❌ 오류 발생: {str(e)}"

# 디자인: 120% 확대하여 하단/측면 로고 영역을 물리적으로 밀어냄 (v2.3)
unicorn_html = """
<div style="display: flex; justify-content: center; align-items: center; width: 100%; overflow: hidden; margin-bottom: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
    <div data-us-project="eX9SsUyi4QA7f2haL3wn" style="width: 100%; max-width: 1440px; height: 400px; transform: scale(1.4); transform-origin: center;"></div>
</div>
<script type="text/javascript">
    (function(){
        if(!window.UnicornStudio){
            window.UnicornStudio={isInitialized:!1};
            var i=document.createElement("script");
            i.src="https://cdn.jsdelivr.net/gh/hiunicornstudio/unicornstudio.js@v1.5.3/dist/unicornStudio.umd.js";
            i.onload=function(){
                if(!window.UnicornStudio.isInitialized){
                    UnicornStudio.init();
                    window.UnicornStudio.isInitialized=!0;
                }
            };
            (document.head || document.body).appendChild(i);
        }
    })();
</script>
"""

def unzip_data(zip_file):
    target_dir = os.path.join(TRAIN_DATA_DIR, "current_dataset")
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    os.makedirs(target_dir, exist_ok=True)
    
    # Gradio 4.x handles file as path string
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(target_dir)
    
    return f"Dataset Extracted to {target_dir}. Ready to train."

def run_training(model_name, epochs, progress=gr.Progress()):
    package_path = os.path.join(TRAIN_DATA_DIR, "current_dataset")
    if not os.path.exists(package_path):
        return "Error: 학습 데이터가 없습니다. 먼저 ZIP 파일을 업로드하고 'Unzip Data' 버튼을 눌러주세요.", None
    
    def progress_wrapper(p, msg):
        progress(p/100, desc=msg)
        
    try:
        model_path = trainer.train(
            package_path=package_path,
            model_name=model_name,
            epochs=int(epochs),
            progress_callback=progress_wrapper
        )
        if model_path:
            return f"Training Complete! Model saved at: {model_path}", model_path
        else:
            return "Training Failed. Check logs.", None
    except Exception as e:
        return f"Error: {str(e)}", None

def run_rvc_conversion(vocal_file, model_path, index_file=None, progress=gr.Progress()):
    if not vocal_file or not model_path:
        return "파일을 선택해주세요.", None
    try:
        progress(0.1, desc="Loading Model...")
        
        # .index 파일 자동 매칭 (index_file이 없으면 같은 폴더에서 찾음)
        final_index = index_file if index_file else get_index_for_model(model_path)
        
        success = converter.load_model(model_path, index_path=final_index)
        if not success:
            return "Failed to load model.", None
            
        output_path = os.path.join(OUTPUT_DIR, f"result_{int(time.time())}.wav")
        progress(0.3, desc="Converting...")
        
        if converter.convert(vocal_file, output_path):
            return "변환 성공!", output_path
        else:
            return "변환 중 오류 발생", None
    except Exception as e:
        return f"에러: {str(e)}", None

def run_mixing(vocal_path, mr_path, vocal_vol, mr_vol, reverb, model_path, use_rvc, progress=gr.Progress()):
    if not vocal_path or not mr_path:
        return "Please upload both Vocal and MR files.", None
    
    try:
        vocal_to_mix = vocal_path
        if use_rvc and model_path:
            progress(0.1, desc="Running RVC Conversion first...")
            rvc_out = os.path.join(OUTPUT_DIR, "temp_rvc_vocal.wav")
            
            # .index 자동 매칭
            idx_path = get_index_for_model(model_path)
            
            if not converter.load_model(model_path, index_path=idx_path):
                return "RVC Model Load Failed!", None
            if converter.convert(vocal_path, rvc_out):
                vocal_to_mix = rvc_out
            else:
                return "RVC Conversion Failed!", None
        
        output_path = os.path.join(OUTPUT_DIR, f"final_mix_{int(time.time())}.mp3")
        def progress_wrapper(p, msg):
            progress(p/100, desc=msg)
            
        success = enhancer.process(
            vocal_path=vocal_to_mix,
            mr_path=mr_path,
            output_path=output_path,
            vocal_volume=vocal_vol,
            mr_volume=mr_vol,
            reverb_amount=reverb,
            progress_callback=progress_wrapper
        )
        
        if success:
            return "Mixing Complete!", output_path
        else:
            return "Mixing Failed.", None
    except Exception as e:
        return f"Error: {e}", None

def run_massive_batch_job(input_folder, model_path):
    if not os.path.exists(input_folder):
        return f"Error: 입력 폴더를 찾을 수 없습니다: {input_folder}"
    if not os.path.exists(model_path):
        return f"Error: 모델 파일을 찾을 수 없습니다: {model_path}"
    if not converter.load_model(model_path):
        return "Error: AI 모델 로드 실패"
        
    batch_out = os.path.join(OUTPUT_DIR, f"batch_{int(time.time())}")
    os.makedirs(batch_out, exist_ok=True)
    
    files = [f for f in os.listdir(input_folder) if f.endswith(('.wav', '.mp3', '.flac'))]
    files.sort()
    
    print(f"🚀 배치 처리 시작: 총 {len(files)}개 파일 발견")
    success_count = 0
    for i, filename in enumerate(files):
        in_path = os.path.join(input_folder, filename)
        out_path = os.path.join(batch_out, f"ai_{filename}")
        print(f"   [{i+1}/{len(files)}] 변환 중: {filename}...")
        try:
            if converter.convert(in_path, out_path):
                success_count += 1
            else:
                print(f"   ⚠️ 실패: {filename}")
        except Exception as e:
            print(f"   ❌ 오류: {filename} ({e})")
            
    return f"✅ 배치 처리 완료! 성공: {success_count}/{len(files)}\n결과 저장: {batch_out}"

# Bento Grid CSS
bento_css = """
body, .gradio-container {
    background-color: #09090b !important;
    color: #e4e4e7 !important; 
    font-family: 'Inter', sans-serif;
}
.bento-card {
    background-color: #18181b !important;
    border: 1px solid #27272a !important;
    border-radius: 24px !important;
    padding: 24px !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
    margin-bottom: 20px !important;
    transition: all 0.3s ease;
}
.bento-card:hover {
    border-color: #3f3f46 !important;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04) !important;
    transform: translateY(-2px);
}
.bento-header {
    font-size: 1.5rem !important;
    font-weight: 700 !important;
    margin-bottom: 1rem !important;
    color: #f4f4f5 !important;
}
/* Controls Styling */
label { color: #a1a1aa !important; font-weight: 500 !important; }
input[type="range"] { accent-color: #8b5cf6 !important; }
button {
    border-radius: 12px !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
}
button.primary {
    background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%) !important;
    border: none !important;
    color: white !important;
}
button.secondary {
    background-color: #27272a !important;
    color: #e4e4e7 !important;
    border: 1px solid #3f3f46 !important;
}
/* Input Fields */
input, textarea, select {
    background-color: #27272a !important;
    border: 1px solid #3f3f46 !important;
    color: white !important;
    border-radius: 8px !important;
}
"""

# UI Build
with gr.Blocks(title="Next-Gen AI Audio Workstation (Bento Edition)", theme=gr.themes.Base(primary_hue="violet", neutral_hue="zinc"), css=bento_css) as app:
    gr.HTML(unicorn_html)
    gr.Markdown("# 🎵 Next-Gen AI Audio Workstation (v2.3)")
    gr.Markdown("Created by **Music Revolutionary JAESOO (SKY Group)**")
    
    with gr.Tab("🎙️ Voice Training"):
        with gr.Column(elem_classes=["bento-card"]):
            gr.Markdown("### Train your own AI Voice Model", elem_classes=["bento-header"])
            with gr.Row():
                train_zip = gr.File(label="Upload Training Data (ZIP of WAVs)", file_types=['.zip'])
                train_btn = gr.Button(value="", icon="https://api.iconify.design/solar:zip-file-bold-duotone.svg")
            unzip_status = gr.Textbox(label="Status", interactive=False)
            train_btn.click(unzip_data, inputs=[train_zip], outputs=[unzip_status])
            
        with gr.Column(elem_classes=["bento-card"]):
            gr.Markdown("### Training Configuration", elem_classes=["bento-header"])
            with gr.Row():
                model_name_input = gr.Textbox(label="Model Name", value="MyVoice")
                epochs_input = gr.Slider(minimum=5, maximum=500, value=100, step=5, label="Epochs (100+ 권장)")
                start_train_btn = gr.Button(value="", variant="primary", icon="https://api.iconify.design/solar:play-circle-bold-duotone.svg")
            train_status = gr.Textbox(label="Training Status")
            train_output_file = gr.File(label="Download Model (.pth)")
            start_train_btn.click(run_training, inputs=[model_name_input, epochs_input], outputs=[train_status, train_output_file])
        
    with gr.Tab("🔄 RVC Conversion"):
        with gr.Column(elem_classes=["bento-card"]):
            gr.Markdown("### Convert Voice & Model Settings", elem_classes=["bento-header"])
            with gr.Row():
                rvc_vocal = gr.Audio(type="filepath", label="Input Vocal File")
                with gr.Column():
                    model_dict = get_model_dict()
                    rvc_model_drop = gr.Dropdown(label="Select AI Voice Model", choices=list(model_dict.keys()), value=list(model_dict.keys())[0] if model_dict else None)
                    
                    # [UI 개설] 현재 매칭된 인덱스 파일 정보 표시
                    rvc_index_info = gr.Markdown("🔍 **Detected Index:** None (Select a model first)")
                    
                    with gr.Accordion("Advanced: Custom Folder / Path Override", open=False):
                        custom_folder_input = gr.Textbox(label="Custom Model Folder Path", placeholder="C:\\MyModels")
                        refresh_models_btn = gr.Button(value="", variant="secondary", icon="https://api.iconify.design/solar:refresh-circle-bold-duotone.svg")
                        manual_model_path = gr.Textbox(label="Manual .pth Path (Override)")
                        manual_index_path = gr.Textbox(label="Manual .index Path (Override)")
                    
                    gr.Markdown("---")
                    rvc_index_file = gr.File(label="Optional: External .index File (Manual Upload)", file_count="single")
        
        with gr.Column(elem_classes=["bento-card"]):
            gr.Markdown("### Conversion Action", elem_classes=["bento-header"])
            rvc_btn = gr.Button(value="", variant="primary", icon="https://api.iconify.design/solar:magic-stick-3-bold-duotone.svg")
            rvc_status = gr.Textbox(label="Status")
            rvc_result = gr.Audio(label="Converted Audio")
        
        def on_model_change(model_sel, custom_p):
            m_dict = get_model_dict(custom_p)
            path = m_dict.get(model_sel)
            idx = get_index_for_model(path)
            if idx:
                return f"✅ **Automatically matched Index:** `{os.path.basename(idx)}`"
            return "⚠️ **No Index Found:** (Retrieval disabled unless uploaded manually)"

        rvc_model_drop.change(on_model_change, inputs=[rvc_model_drop, custom_folder_input], outputs=rvc_index_info)
        
        def update_models(custom_p):
            new_dict = get_model_dict(custom_p)
            new_choices = list(new_dict.keys())
            new_val = new_choices[0] if new_choices else None
            return (
                gr.update(choices=new_choices, value=new_val), 
                gr.update(choices=new_choices, value=new_val),
                gr.update(choices=new_choices, value=new_val)
            )
        
        def handle_rvc_conversion(vocal, model_sel, index_up, m_path, m_index, custom_p):
            m_dict = get_model_dict(custom_p)
            # 수동 경로 우선, 없으면 드롭다운 선택값 사용
            final_model = m_path if m_path and os.path.exists(m_path) else m_dict.get(model_sel)
            # 수동 인덱스 경로 우선, 없으면 업로드된 파일, 없으면 자동 매칭
            final_index = m_index if m_index and os.path.exists(m_index) else index_up
            
            return run_rvc_conversion(vocal, final_model, final_index)


        rvc_btn.click(handle_rvc_conversion, 
                      inputs=[rvc_vocal, rvc_model_drop, rvc_index_file, manual_model_path, manual_index_path, custom_folder_input], 
                      outputs=[rvc_status, rvc_result])
        
    with gr.Tab("🎛️ AI Studio Mixing"):
        with gr.Column(elem_classes=["bento-card"]):
            gr.Markdown("### Mix Vocals + MR", elem_classes=["bento-header"])
            with gr.Row():
                mix_vocal = gr.Audio(type="filepath", label="Vocal Track")
                mix_mr = gr.Audio(type="filepath", label="MR / Instrumental")
            with gr.Accordion("AI Voice Conversion Settings (Optional)", open=False):
                use_rvc_chk = gr.Checkbox(label="Enable RVC Conversion before Mixing", value=False)
                mix_model_dict = get_model_dict()
                mix_model_drop = gr.Dropdown(label="Select RVC Model", choices=list(mix_model_dict.keys()), value=list(mix_model_dict.keys())[0] if mix_model_dict else None)
        
        with gr.Column(elem_classes=["bento-card"]):
            gr.Markdown("### Mixing Controls", elem_classes=["bento-header"])
            with gr.Row():
                vol_vocal = gr.Slider(-10, 10, value=0, label="Vocal Volume (dB)")
                vol_mr = gr.Slider(-10, 10, value=0, label="MR Volume (dB)")
                reverb_amt = gr.Slider(0, 100, value=30, label="Reverb (ms)")
            mix_btn = gr.Button(value="", variant="primary", icon="https://api.iconify.design/solar:music-note-slider-2-bold-duotone.svg")
            mix_status = gr.Textbox(label="Status")
            mix_result = gr.Audio(label="Final Mix")
        
        def handle_mixing(v_p, m_p, v_v, m_v, rev, model_sel, use_rvc, custom_p):
            m_dict = get_model_dict(custom_p)
            final_model = m_dict.get(model_sel)
            return run_mixing(v_p, m_p, v_v, m_v, rev, final_model, use_rvc)



    with gr.Tab("🛠️ Model Tools"):
        with gr.Column(elem_classes=["bento-card"]):
            gr.Markdown("### Advanced Model Management", elem_classes=["bento-header"])
            with gr.Row():
                with gr.Column():
                    gr.Markdown("#### 📦 Create .index File (Features Retrieval)")
                    gr.Markdown("기존 모델에 .index 파일이 없는 경우, 학습 데이터셋을 사용하여 새로 생성합니다.")
                    tool_model_dict = get_model_dict()
                    tool_model_drop = gr.Dropdown(label="선택된 모델", choices=list(tool_model_dict.keys()), value=list(tool_model_dict.keys())[0] if tool_model_dict else None)
                    tool_dataset_path = gr.Textbox(label="학습 데이터셋 폴더 경로", value=os.path.join(TRAIN_DATA_DIR, "current_dataset"))
                    tool_index_btn = gr.Button(value="", variant="primary", icon="https://api.iconify.design/solar:database-bold-duotone.svg")
                    tool_index_status = gr.Textbox(label="결과")
                    
                    def run_idx_tool(m_sel, d_p):
                        m_dict = get_model_dict()
                        m_path = m_dict.get(m_sel)
                        return generate_index_manually(m_path, d_p)
                    
                    tool_index_btn.click(run_idx_tool, inputs=[tool_model_drop, tool_dataset_path], outputs=[tool_index_status])

    # Event Listeners (Moved here to avoid NameError)
    refresh_models_btn.click(update_models, inputs=[custom_folder_input], outputs=[rvc_model_drop, mix_model_drop, tool_model_drop])
    mix_btn.click(handle_mixing, inputs=[mix_vocal, mix_mr, vol_vocal, vol_mr, reverb_amt, mix_model_drop, use_rvc_chk, custom_folder_input], outputs=[mix_status, mix_result])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Next-Gen AI Audio Workstation")
    parser.add_argument("--batch_mode", action="store_true", help="Run in batch mode without UI")
    args = parser.parse_args()

    if args.batch_mode:
        print("\n" + "="*60)
        print("🚀 BATCH MODE ACTIVE (Massive Overnight Processing)")
        print("="*60)
        batch_input = os.path.join(BASE_DIR, "batch_input")
        os.makedirs(batch_input, exist_ok=True)
        model_list = [f for f in os.listdir(MODELS_DIR) if f.endswith('.pth')]
        if not model_list:
            print("❌ [ERROR] 'models' 폴더에 .pth 파일이 없습니다.")
            sys.exit(1)
        target_model = os.path.join(MODELS_DIR, model_list[0])
        print(f"[INFO] 모델: {target_model}")
        print(f"[INFO] 입력 폴더: {batch_input}")
        result = run_massive_batch_job(batch_input, target_model)
        print(f"\n{result}")
        print("======================================================\n")
        time.sleep(2) 
    else:
        app.queue().launch(share=True)