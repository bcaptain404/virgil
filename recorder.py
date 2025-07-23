import time
import subprocess
import time
from logger import log
import sounddevice as sd
import numpy as np

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

