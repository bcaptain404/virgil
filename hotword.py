import time
import os
import pvporcupine
import sounddevice as sd
import struct
from logger import log

porcupine = None
stream = None
wake_callback = None

def init_hotword(config):
    global porcupine, stream
    keyword_path = config.get("wake_word_model")
    access_key = config.get("porcupine_access_key")

    if not access_key:
        raise ValueError("Porcupine access_key is required. Set it in config.json or .env")

    if keyword_path and os.path.exists(keyword_path):
        porcupine = pvporcupine.create(
            access_key=access_key,
            keyword_paths=[keyword_path]
        )
        log(f"[{time.time()}] 🔑 Custom wake word loaded from {keyword_path}")
    else:
        porcupine = pvporcupine.create(
            access_key=access_key,
            keywords=["porcupine"]
        )
        log(f"[{time.time()}] ⚠️ Using default wake word: 'porcupine'")

    stream = sd.InputStream(
        channels=1,
        samplerate=porcupine.sample_rate,
        blocksize=porcupine.frame_length,
        dtype="int16",
        callback=audio_callback
    )
    stream.start()
    log(f"[{time.time()}] 👂 Hotword detection initialized.")

def audio_callback(indata, frames, time_info, status):
    pcm = struct.unpack_from("%dh" % len(indata), indata)
    keyword_index = porcupine.process(pcm)
    if keyword_index >= 0:
        log(f"[{time.time()}] 🔊 Wake word detected!")
        on_wake()

def on_wake():
    if wake_callback:
        wake_callback()

def register_callback(callback):
    global wake_callback
    wake_callback = callback

def stop_hotword():
    if stream:
        stream.stop()
    if porcupine:
        porcupine.delete()
