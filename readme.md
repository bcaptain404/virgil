# Virgil: Offline Voice Assistant

This is not ready for general use yet. The build scrits are a work-in-progress as well.

## 🧱 Project Structure
- Modular Python architecture
- Fully offline speech-to-text + text-to-speech loop
- Wake word detection ("Virgil") via Porcupine

## 📦 Dependencies
Below This is a VERY rough build procedure, you may have to tailor it to your setup, OS, or distro.
Seriously, it needs a lot of work... but ... we'll work on it as the project progresses.
```
# if on Ubuntu:
sudo apt install -y alsa-utils build-essential cmake curl ffmpeg libbz2-dev libffi-dev\
    libgdbm-dev liblzma-dev libncurses5-dev libnss3-dev libopenblas-dev libreadline-dev\
    libsoundio-dev libsqlite3-dev libssl-dev portaudio19-dev python3-dev sox tk-dev\
    uuid-dev wget zlib1g-dev

# NOTE: python 3.12 is required (not newer [yet])
# NOTE: Running in a venv is recommended, but that is beyond the scope of this document.

# if on Ubuntu 24.10:
apt install python3

# If on Ubuntu 25.04 (run `cat /etc/issue` to find out), the packaged python3 is too new. However, you can install python 3.12 as an alternative to whatever version is already installed:
cd /usr/src
sudo wget https://www.python.org/ftp/python/3.12.3/Python-3.12.3.tgz && \
    sudo tar -xf Python-3.12.3.tgz && \
    cd Python-3.12.3 && \
    sudo ./configure --enable-optimizations --with-ensurepip=install && \
    sudo make -j$(nproc) && sudo make altinstall
sudo update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.12 1
sudo update-alternatives --config python3
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.13 2 # select python 3.12
python3 --version # confirm you're running python 3.12

# Here's the rough idea on how to create a venv:
python3 -m venv ~/virgil-env
source ~/virgil-env/bin/activate

# install pip
python3 -m ensurepip --upgrade

# Install Python dependencies:
/usr/local/bin/python3.12 -m pip install coqui-tts coqui-tts python-dotenv pvporcupine sounddevice
/usr/local/bin/python3.12 -m pip install ffmpeg-python # development dependencied (if wanted)

# Bonus: If you're still confused, look into pipx for installing python3 dependencies globally. That's sometimes an option.

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

