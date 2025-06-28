# Virgil: Offline Voice Assistant

This is not ready for general use yet. The build scrits are a work-in-progress as well.

## 🧱 Project Structure
- Modular Python architecture
- Fully offline speech-to-text + text-to-speech loop
- Wake word detection ("Virgil") via Porcupine

## 📦 Python Dependencies
Install via pip:
```
TTS
python-dotenv
pvporcupine
sounddevice
```
Optional (for development):
```
ffmpeg-python
```

## 🛠️ Ubuntu/Linux System Dependencies
Install via apt:
```bash
ffmpeg
build-essential
cmake
libopenblas-dev
libsoundio-dev
portaudio19-dev
alsa-utils
sox        # optional (beep generation)
python3-dev
```

## 🗂 Config Files
- `.env` — optional environment overrides
- `config.json` — project-wide config for paths and settings

## 🔁 Runtime Logs
- `virgil.log` — auto-rotated log with timestamps
- `virgil.log.old` — previous session log

## ✅ Current Features
- Whisper STT integration
- Coqui TTS voice synthesis
- Keyword detection with Porcupine
- Config via env, JSON, and CLI
- Modular codebase (`main.py`, `config.py`, `logger.py`, etc.)

---
To add a new dependency, update this file and install accordingly.

