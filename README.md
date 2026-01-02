# 🎵 Next-Gen AI Audio Workstation

**Professional 6-Stem Separation, AI Voice Training, and Automatic Score Generation System**

Created by **Music Revolutionary JAESOO**

---

## 🚀 Quick Start (One-Click Setup)

We have simplified the installation process. Just follow these steps:

1.  **Run `setup.bat`**: Double-click this file. It will automatically:
    *   Install Python dependencies (PyTorch with CUDA, etc.)
    *   Download FFmpeg and LilyPond
    *   Setup the entire environment
2.  **Run `run_gui.bat`**: Start the application!

> 📖 **Need more details?** Read **[setup.md](setup.md)** for a comprehensive guide.

---

## ✨ Key Features

### 1. 🎧 Ultimate Separation (6-Stem)
Separate any song into **Vocals, Drums, Bass, Guitar, Piano, and Others**.
*   **Engine**: Demucs Hybrid Model (High Quality)
*   **Output**: Individual WAV files for professional mixing.

### 2. 🎼 Automatic Score Generation
Convert your audio directly into sheet music!
*   **Format**: MusicXML, PDF, and High-Res PNG.
*   **Engine**: Integrated LilyPond & Music21 pipeline.
*   **Support**: Full band score generation (Drum tab, Bass clef, Treble clef).

### 3. 🎙️ AI Voice Training & Cover
*   **Train**: Create a custom AI voice model using your own recordings.
*   **Cover**: Convert any song's vocals into your trained voice.
*   **Tech**: RVC (Retrieval-based Voice Conversion) & GPT-SoVITS.

### 4. 🎚️ Professional Audio Effects
*   **Dolby Style**: 3D Surround Sound & Crystalizer.
*   **Hi-Fi Mode**: Audio upscaling and noise reduction.

---

## 💻 System Requirements

*   **OS**: Windows 10/11 (64-bit)
*   **GPU**: NVIDIA GeForce GTX 1060 or higher (Recommended for fast processing)
*   *Note: CPU mode is supported but slower.*
*   **RAM**: 16GB Recommended

## 📂 Project Structure
*   `ffmpeg/`: Audio processing engine
*   `output_result/`: All generated files (Audio, MIDI, Scores) saved here
*   `models/`: AI models storage
*   `venv/`: Python virtual environment

---
*Enjoy your music revolution!*