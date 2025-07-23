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

def select_input_device(config_path, force_select=False):
    log(f"[{time.time()}] 🎙 Checking available input devices...")
    devices = sd.query_devices()
    input_devices = [d for d in devices if d['max_input_channels'] > 0]

    if not input_devices:
        log(f"[{time.time()}] ❌ No microphone input devices found.")
        exit(1)

    # Load config
    with open(config_path, 'r') as f:
        config = json.load(f)
        selected = None

        requested_name = ""
        if force_select:
            log(f"[{time.time()}] 🔁 Forcing audio device selection.")
        else:
            requested_name = config.get("audio_input_name", "").strip()

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
                dev_name = dev['name']
                host_api = dev.get('hostapi', 'N/A')
                max_channels = dev['max_input_channels']
                log(f"   [{idx}] {dev_name} (Channels: {max_channels})")

            print("\nAvailable Microphones:")
            for idx, dev in enumerate(input_devices):
                print(f"[{idx}] {dev['name']} - {dev['max_input_channels']} channel(s)")

            while True:
                try:
                    choice = int(input("Select mic input by number: "))
                    if 0 <= choice < len(input_devices):
                        selected = input_devices[choice]['name']
                        log(f"[{time.time()}] 🧠 User selected: {selected}")
                        break
                    else:
                        print("Out of range. Try again.")
                except Exception:
                    print("Invalid input. Try again.")

        log(f"[{time.time()}] 🎤 Selected input device: {selected}")
        log(f"[{time.time()}] 💾 Updating config with selected mic device.")
        config["audio_input_name"] = selected # Update config with selected device name
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)

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

