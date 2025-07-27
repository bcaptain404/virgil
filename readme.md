# Virgil: Offline Voice Assistant

This is not ready for general use yet. The build scripts are a work in progress.

## 🧱 Project Structure
- Modular Python architecture
- Fully offline speech-to-text + text-to-speech loop
- Wake word detection ("Virgil") via Porcupine

## 📦 Dependencies

> ⚠️ This section is a work-in-progress. It works on Ubuntu 24.10+, but you'll need to adjust if you're using something cursed or ancient.

### 🧱 System Packages
```bash
sudo apt install -y alsa-utils build-essential cmake curl ffmpeg libbz2-dev libffi-dev \
    libgdbm-dev liblzma-dev libncurses5-dev libnss3-dev libopenblas-dev libreadline-dev \
    libsoundio-dev libsqlite3-dev libssl-dev portaudio19-dev python3-dev sox tk-dev \
    uuid-dev wget zlib1g-dev
```

### 🐍 Python 3.12 Installation (if your distro ships Python 3.13+)
```bash
cd /usr/src
sudo wget https://www.python.org/ftp/python/3.12.3/Python-3.12.3.tgz
sudo tar -xf Python-3.12.3.tgz
cd Python-3.12.3
sudo ./configure --enable-optimizations --with-ensurepip=install
sudo make -j$(nproc)
sudo make altinstall
```

### 🔀 Enable Python 3.12 via update-alternatives:
```bash
sudo update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.12 1
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.13 2
sudo update-alternatives --config python3   # Choose Python 3.12 from the menu
python3 --version                           # Should now show 3.12.x
```

---

### 🦪 Setup Global Virgil Venv
We recommend a global-ish venv to avoid fighting Ubuntu's Python packaging. For example:
```bash
python3 -m venv ~/.local/fuck-ubuntu
source ~/.local/fuck-ubuntu/bin/activate
```

You can add this to your `.bashrc`:
```bash
# Activate Virgil env automatically
source ~/.local/fuck-ubuntu/bin/activate
```

---

### 📦 Python Package Installs (from within the venv):

```bash
# Required
pip install coqui-tts python-dotenv pvporcupine sounddevice

# Optional (for audio post-processing)
pip install ffmpeg-python
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

