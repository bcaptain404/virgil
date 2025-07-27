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

    DEFAULT_WAKE_SENS = 0.6
    wake_sensitivity = config.get("wake_sensitivity", DEFAULT_WAKE_SENS)
    input_device = config.get("audio_input")

    log(f"[{time.time()}] 🎙️ Using input_device_index: {input_device}")

    if keyword_path and os.path.exists(keyword_path):
        log(f"[{time.time()}] 🔑 Custom wake word loaded from {keyword_path}")
        porcupine = pvporcupine.create(
            access_key=access_key,
            keyword_paths=[keyword_path],
            sensitivities=[wake_sensitivity]
        )
    else:
        log(f"[{time.time()}] ⚠️ Using default wake word: 'porcupine'")
        porcupine = pvporcupine.create(
            access_key=access_key,
            keywords=["porcupine"],
            sensitivities=[wake_sensitivity]
        )

    info = pyaudio_instance.get_device_info_by_index(input_device_index)
    log(f"🔍 Using device: {info['name']} @ {info['defaultSampleRate']} Hz")

    stream = sd.InputStream(
        device=input_device,
        channels=1,
        samplerate=porcupine.sample_rate,
        blocksize=porcupine.frame_length,
        dtype="int16",
        callback=audio_callback
    )

    log(f"[{time.time()}] 🎤 Using input device: {input_device}")
    stream.start()
    log(f"🎧 Starting mic stream with index={input_device_index}, sample_rate={sample_rate}, channels=1, format=paInt16")
    log(f"[{time.time()}] 👂 Hotword detection initialized.")

def audio_callback(indata, frames, time_info, status):
    log(f"[{time.time()}] 🎧 Listening...")
    pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
    pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
    if suppress_wake.is_set():
        log(f"[{time.time()}] ⏸ Wake suppressed.")
    else:
        result = porcupine.process(pcm)
        log(f"[{time.time()}] 👂 Wake result: {result}")
        if result >= 0:
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
