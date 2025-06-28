#!/bin/bash

set -e

echo "🔧 [Virgil] Installing system dependencies..."

# Update package list
sudo apt update

# Install core system packages
sudo apt install -y \
    python3 \
    python3-venv \
    python3-pip \
    git \
    build-essential \
    ffmpeg \
    libsndfile1 \
    curl \
    unzip

# Optional: tools for future use
sudo apt install -y sox libsox-fmt-all

echo "✅ [Virgil] System packages installed."

# Set up virtual environment
echo "🐍 [Virgil] Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "📦 [Virgil] Installing Python packages..."
pip install --upgrade pip
pip install \
    openai-whisper \
    torchaudio \
    sounddevice \
    numpy \
    requests \
    beautifulsoup4 \
    pydub

echo "✅ [Virgil] Python packages installed."

echo "📁 [Virgil] Initializing git repository..."
git init
echo "venv/" >> .gitignore
echo "*.log" >> .gitignore
git add .
git commit -m "Initial commit: bootstrap install script and main runner"

echo "🎉 [Virgil] Setup complete. Activate the virtualenv with: source venv/bin/activate"
