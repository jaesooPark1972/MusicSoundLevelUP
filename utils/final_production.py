import os
import requests
import re
import music21
import subprocess
import sys

# ========================================================
# [설정] LilyPond 경로 (Portable 및 기본 경로 체크)
# ========================================================
current_dir = os.path.dirname(os.path.abspath(__file__))
LILYPOND_EXE = os.path.join(current_dir, "lilypond-2.24.4", "bin", "lilypond.exe")
if not os.path.exists(LILYPOND_EXE):
    LILYPOND_EXE = r"C:\lilypond-2.24.4\bin\lilypond.exe"

# --------------------------------------------------------
# 1. Suno 가사 가져오기 (해킹 모듈)
# --------------------------------------------------------
# [FIX] Force ASCII output
import io
import time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='ascii', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='ascii', errors='replace')

# --------------------------------------------------------
# 1. Suno Lyrics Fetcher
# --------------------------------------------------------
def get_suno_lyrics(suno_url):
    if not suno_url or "suno" not in suno_url:
        return None
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    print(f"[INFO] Connecting to Suno server...")
    
    # [FIX] URL ID extraction
    song_id_match = re.search(r"(?:song/|s/|playlist/)([a-zA-Z0-9\-]+)", suno_url)
    if not song_id_match:
        song_id_match = re.search(r"/([a-zA-Z0-9\-]+)$", suno_url.split('?')[0])
    
    if not song_id_match: return None
    
    song_id = song_id_match.group(1)
    
    # Short ID handling
    if len(song_id) < 30:
        try:
            r = requests.get(suno_url, headers=headers, allow_redirects=True, timeout=5)
            id_match = re.search(r"song/([a-f0-9\-]{32,})", r.url)
            if id_match: song_id = id_match.group(1)
        except: pass

    api_url = f"https://studio-api.suno.ai/api/feed/?ids={song_id}"
    
    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data:
                metadata = data[0].get('metadata', {})
                lyrics = metadata.get('prompt', '')
                return lyrics
    except Exception as e:
        print(f"Lyrics Error: {e}")
    return None

# --------------------------------------------------------
# 2. Score Production Engine
# --------------------------------------------------------
def run_production():
    print("\n" + "="*40)
    print("= AI Score Production System (Final)")
    print("="*40)

    # 1. Input
    print("Enter Suno link (Enter to skip): ", end="")
    suno_url = sys.stdin.readline().strip().rstrip(':').rstrip('/')
    
    lyrics_text = ""
    if suno_url:
        lyrics_text = get_suno_lyrics(suno_url)
        if lyrics_text:
            print(f"[OK] Lyrics acquired ({len(lyrics_text)} chars)")
        else:
            print("[WARNING] Could not fetch lyrics.")
    else:
        print("[INFO] Proceeding without lyrics.")

    if lyrics_text:
        lyrics_text = re.sub(r'\[.*?\]', '', lyrics_text)
        lyrics_list = [char for char in lyrics_text if char.strip()]
    else:
        lyrics_list = []

    # 2. Folder Lookup
    base_dir = os.path.join(current_dir, "output_result")
    if not os.path.exists(base_dir):
        print(f"[ERROR] Result folder not found: {base_dir}")
        return

    all_subdirs = [os.path.join(base_dir, d) for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    if not all_subdirs:
        print("[ERROR] No work history found.")
        return
        
    latest_folder = max(all_subdirs, key=os.path.getmtime)
    midi_folder = os.path.join(latest_folder, "미디분리")
    
    if not os.path.exists(midi_folder):
        print(f"[ERROR] MIDI folder not found: {midi_folder}")
        return

    print(f"[DIR] Target folder: {midi_folder}")

    # 3. Track Processing
    midi_files = [f for f in os.listdir(midi_folder) if f.endswith(".mid")]
    
    found_vocal = False
    for midi_file in midi_files:
        if "vocals" in midi_file.lower():
            found_vocal = True
            print(f"\n[OK] Processing Vocal Track: {midi_file}")
            full_midi_path = os.path.join(midi_folder, midi_file)
            
            try:
                # [Clean Parse] Flatten to remove MIDI artifacts
                s = music21.converter.parse(full_midi_path)
                s = s.flatten().notesAndRests.stream()
                
                # [Pitch Normalization] Fix excessive ledger lines
                avg_pitch = s.analyze('pitch')
                if avg_pitch and avg_pitch.ps > 84: s = s.transpose(-12)
                elif avg_pitch and avg_pitch.ps < 36: s = s.transpose(12)
                
                # [Clef Assignment]
                s.insert(0, music21.clef.TrebleClef())

                # [Robust Quantization]
                s.quantize([4, 3], processOffsets=True, processDurations=True, inPlace=True)
                s.makeMeasures(inPlace=True)
                s.makeRests(fillGaps=True, inPlace=True)
                if not s.recurse().getElementsByClass(music21.meter.TimeSignature):
                    s.measure(1).insert(0, music21.meter.TimeSignature('4/4'))

                # A. Mapping lyrics
                if lyrics_list:
                    print("   - Mapping lyrics (Clean)...")
                    lyric_idx = 0
                    for n in s.recurse().notes:
                        if n.isNote and n.duration.quarterLength >= 0.2:
                            if lyric_idx < len(lyrics_list):
                                n.lyric = lyrics_list[lyric_idx]
                                lyric_idx += 1
                
                # B. Rendering Preview
                clean_name = "Vocal_Score_Lyrics"
                ly_path = os.path.join(midi_folder, "temp_vocal.ly")
                s.write('lily.ly', fp=ly_path)
                
                if os.path.exists(ly_path):
                    # C. Header Refinement
                    with open(ly_path, 'r', encoding='utf-8') as f: content = f.read()
                    
                    title = os.path.basename(latest_folder)
                    header = f"""
\\version "2.24.0"
#(set-global-staff-size 19)
\\paper {{
    #(set-paper-size "a4")
    top-margin = 15\\mm
    bottom-margin = 15\\mm
    left-margin = 15\\mm
    right-margin = 15\\mm
}}
\\header {{
    title = "{title}" 
    subtitle = "Vocal Score with Lyrics"
    composer = "Park Jae-soo (SKY Group)"
    tagline = ##f
}}
"""
                    final_content = header + "\n" + content.replace('\\version "2.24.0"', "").replace('\\version "2.24.2"', "")
                    with open(ly_path, 'w', encoding='utf-8') as f: f.write(final_content)

                    # D. Generation
                    print("   - Factory Running (LilyPond)...")
                    cmd = [
                        LILYPOND_EXE,
                        "-dresolution=300",
                        "--pdf",
                        "--png",
                        "-o", os.path.join(midi_folder, clean_name),
                        ly_path
                    ]
                    
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    subprocess.run(cmd, check=False, startupinfo=startupinfo)
                    
                    # E. Finished
                    png_file = os.path.join(midi_folder, f"{clean_name}.png")
                    psd_file = os.path.join(midi_folder, f"{clean_name}.psd")
                    
                    if os.path.exists(png_file):
                        if os.path.exists(psd_file): os.remove(psd_file)
                        os.rename(png_file, psd_file)
                        print(f"   [SUCCESS] Saved: {clean_name}.pdf / .psd")
                    
                    if os.path.exists(ly_path): 
                        try: os.remove(ly_path)
                        except: pass
                
            except Exception as e:
                print(f"   [ERROR] Processing failed: {e}")

    if not found_vocal:
        print("⚠️ 'vocals' 포함 MIDI 파일을 찾지 못했습니다.")

if __name__ == "__main__":
    run_production()
