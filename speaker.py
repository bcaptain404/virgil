import time
from TTS.api import TTS
import subprocess
from logger import log
from threading import Thread
import torch

_tts = None

def init_tts(config):
    global _tts
    if _tts is None:
        log(f"[{time.time()}] 🎙️ Initializing TTS model...")
        _tts = TTS(model_name=config["tts_model"], progress_bar=False, gpu=True)
        log(f"[{time.time()}] ✅ TTS model loaded.")
        log(f"[{time.time()}] 🧠 TTS object: {id(_tts)}")
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        log(f"[{time.time()}] 🎯 TTS running on: {device}")
        log(f"[{time.time()}] 🧠 CUDA available: {torch.cuda.is_available()}")
        log(f"[{time.time()}] 🔍 Torch backend: {torch.backends.mkldnn.enabled}")

def speak(text, config):
    log(f"[{time.time()}] 🗣 Sending to external TTS subprocess: {text}")
    subprocess.run([
        "python3", "speak_once.py", text
    ])
    #thread = Thread(target=_speak_sync, args=(text, config))
    #thread.start()

def _speak_sync(text, config):
    global _tts
    output_path = config["audio_output"]
    log(f"[{time.time()}] 🧠 TTS object: {id(_tts)}")
    log(f"[{time.time()}] 🗣️ Virgil: {text}")
    try:
        log(f"[{time.time()}] 🗣️ tts_to_file: begin")
        _tts.tts_to_file(text=text, file_path=output_path)
        log(f"[{time.time()}] 🗣️ tts_to_file: done")
        log(f"[{time.time()}] 🗣️ subprocess: begin")
        subprocess.run(["aplay", output_path])
        log(f"[{time.time()}] 🗣️ subprocess: done")
    except Exception as e:
        log(f"[{time.time()}] ❌ TTS failed: {e}")
