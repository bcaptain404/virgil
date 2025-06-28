import sys
import subprocess
import time
from TTS.api import TTS
from logger import log
log(f"[{time.time()}] 🎙️ speak_once.py executing...")
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")
tts.to("cuda")  # or "cpu"
log(f"[{time.time()}] 🎙️ tts_to_file...")
tts.tts_to_file(text=sys.argv[1], file_path="out.wav")
log(f"[{time.time()}] 🎙️ running aplay...")
subprocess.run(["aplay", "out.wav"])
log(f"[{time.time()}] 🎙️ aplay finished.")


