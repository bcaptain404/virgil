import time
import subprocess
from logger import log
import sounddevice as sd
import numpy as np
import json
import os

def select_input_device(config_path):
    log(f"[{time.time()}] 🎙 Checking available input devices...")
    devices = sd.query_devices()
    input_devices = [d for d in devices if d['max_input_channels'] > 0]

    if not input_devices:
        log(f"[{time.time()}] ❌ No microphone input devices found.")
        exit(1)

    # Load config
    with open(config_path, 'r') as f:
        config = json.load(f)

    requested_name = config.get("audio_input_name", "").strip()
    selected = None

    if requested_name:
        log(f"[{time.time()}] 🔍 Config specified input: '{requested_name}'")
        for dev in input_devices:
            if requested_name.lower() in dev['name'].lower():
                selected = dev['name']
                log(f"[{time.time()}] ✅ Found matching input: {selected}")
                break
        if not selected:
            log(f"[{time.time()}] ⚠️ Config input '{requested_name}' not found among active devices.")

    if not selected:
        if len(input_devices) == 1:
            selected = input_devices[0]['name']
            log(f"[{time.time()}] 🎯 Only one input device found. Using: {selected}")
        else:
            log(f"[{time.time()}] 🧭 Multiple input devices detected:")
            for idx, dev in enumerate(input_devices):
                log(f"   [{idx}] {dev['name']}")
            while True:
                try:
                    choice = int(input("Select input device by number: "))
                    if 0 <= choice < len(input_devices):
                        selected = input_devices[choice]['name']
                        log(f"[{time.time()}] 🧠 User selected: {selected}")
                        break
                except Exception:
                    print("Invalid input. Try again.")

        # Update config with selected device name
        config["audio_input_name"] = selected
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        log(f"[{time.time()}] 💾 Updated config with selected mic device.")

    return selected

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

