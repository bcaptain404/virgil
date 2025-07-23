import time
from TTS.api import TTS
import subprocess
from logger import log
import torch
import re
from subprocess import Popen
from threading import Event
import os

suppress_wake = Event()
tts_proc = None
WAKE_WORD = "Virgil"

def sanitize_output(text):
    return re.sub(rf"\b{WAKE_WORD}\b", "I", text, flags=re.IGNORECASE)

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
    global tts_proc, _tts

    text = sanitize_output(text)

    if not text.strip().endswith((".", "!", "?")):
        text += "."

    suppress_wake.set()
    log(f"[{time.time()}] 🗣️ Speaking: {text}")

    output_path = config["audio_output"]

    try:
        start = time.time()
        _tts.tts_to_file(text=text, file_path=output_path)
        log(f"[{time.time()}] 🧾 TTS generation took {time.time() - start:.2f}s")

        # make sure file is finished being written
        prev_size = -1
        while True:
            size = os.path.getsize(output_path)
            if size == prev_size:
                break
            prev_size = size
            time.sleep(0.05)
        log(f"[{time.time()}] 🧾 TTS generation file written.")
    except Exception as e:
        log(f"[{time.time()}] ❌ TTS synthesis failed: {e}")
        suppress_wake.clear()
        return

    try:
        tts_proc = Popen([
            "ffplay", "-nodisp", "-autoexit", output_path
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        tts_proc.wait()
    except Exception as e:
        log(f"[{time.time()}] ❌ Audio playback failed: {e}")
    finally:
        tts_proc = None
        suppress_wake.clear()
