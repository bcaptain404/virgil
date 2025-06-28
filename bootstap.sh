#!/bin/bash
set -e

# NOTE: This script is a work-in-progress.

#TODO: Python Dependencies (recheck readme.md)
#pip Install TTS python-dotenv pvporcupine sounddevice

# todo: recheck readme.md for deps
apt install \
    ffmpeg \
    build-essential \
    cmake \
    libopenblas-dev \
    libsoundio-dev \
    portaudio19-dev \
    alsa-utils \
    sox \
    python3-dev
    sudo \
    apt \
    install \
    python3-venv \
    python3-pip \
    -y

# todo: git clone whisper.cpp
./build-whisper.sh

# todo: download whisper models

# todo: 
python3 -m venv ~/virgil-env
source ~/virgil-env/bin/activate
pip install --upgrade pip
pip install TTS

#todo: create porcupine account and hotword
