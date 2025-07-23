import time
import subprocess
from logger import log
import sounddevice as sd
import numpy as np
import json
import os

def get_device_index_by_name(name):
    for idx, dev in enumerate(sd.query_devices()):
        if name.lower() in dev['name'].lower():
            return idx
    return None

def select_input_device(config, override=False):
    input_devices = sd.query_devices()
    input_list = [d for d in input_devices if d["max_input_channels"] > 0]

    log(f"[{time.time()}] 🎙 Found {len(input_list)} input devices.")

    if not input_list:
        log(f"[{time.time()}] ❌ No input devices found. Exiting.")
        exit(1)

    if override or "audio_input_name" not in config or not config["audio_input_name"]:
        log(f"[{time.time()}] 🔧 Forcing device selection...")
        for i, device in enumerate(input_list):
            log(f"{i}: {device['name']}")

        selection = input(f"Select input device [0-{len(input_list)-1}]: ")
        index = int(selection)
        device_name = input_list[index]["name"]
        config["audio_input_name"] = device_name

        with open(config["config_path"], "w") as f:
            json.dump(config, f, indent=2)

        log(f"[{time.time()}] ✅ Saved selected input device: {device_name}")

    config["audio_input"] = get_device_index_by_name(config["audio_input_name"])
    log(f"[{time.time()}] ✅ Using configured input device: {config['audio_input_name']} at device number {config['audio_input']}")
    return config["audio_input_name"], config["audio_input"]

def check_microphone_activity(device=None, duration=2.0, threshold=0.01):
    """
    Records briefly and checks if mic is picking up audio above a noise threshold.
    Returns True if mic appears functional, False otherwise.
    """
    try:
        log(f"[{time.time()}] 🎙️ Checking mic input (device={device})...")
        recording = sd.rec(int(duration * 16000), samplerate=16000, channels=1, dtype='float32', device=device)
        sd.wait()

        peak_amplitude = np.max(np.abs(recording))
        log(f"[{time.time()}] 📊 Mic peak amplitude: {peak_amplitude:.5f}")

        if peak_amplitude > threshold:
            log(f"[{time.time()}] ✅ Mic appears to be working.")
            return True
        else:
            log(f"[{time.time()}] ⚠️ Mic input too quiet or silent.")
            return False

    except Exception as e:
        log(f"[{time.time()}] ❌ Mic check failed: {e}")
        return False

def record_audio(filename, duration):
    log(f"[{time.time()}] 🎙️ Recording audio to {filename} for {duration} seconds...")
    subprocess.run([
        "arecord",
        "-d", str(duration),
        "-f", "S16_LE",
        "-r", "16000",
        "-c", "1",
        filename
    ], check=True)
    time.sleep(0.25)  # small pause before starting STT

