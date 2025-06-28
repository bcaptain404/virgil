import time
import threading
import subprocess
import os
import queue
import time
from speaker import speak
from logger import log

_job_queue = queue.Queue()
_config = None

def start_worker(config):
    global _config
    _config = config
    thread = threading.Thread(target=_worker_loop, daemon=True)
    thread.start()
    log(f"[{time.time()}] 🧵 Whisper transcription worker started.")

def enqueue_transcription(audio_path):
    log(f"[{time.time()}] ⏳ Transcribing from: {os.path.abspath(audio_path)}")
    log(f"[{time.time()}] 🔧 CWD: {os.getcwd()}")
    _job_queue.put(audio_path)
    log(f"[{time.time()}] 📥 Enqueued audio for transcription: {audio_path}")

def _worker_loop():
    while True:
        audio_path = _job_queue.get()
        try:
            transcript_file = _config["transcription_file"]
            whisper_bin = _config["whisper_bin"]
            whisper_model = _config["whisper_model"]

            result = subprocess.run(
                [
                    whisper_bin,
                    "-m", whisper_model,
                    "-f", os.path.abspath(audio_path),
                    "--output-txt",
                    "-of", "transcription"
                ],
                cwd=_config["whisper_dir"],
                capture_output=True,
                text=True
            )

            if result.stderr:
                log(f"[{time.time()}] 📛 Whisper STDERR:\n{result.stderr}")

            if os.path.exists(transcript_file):
                with open(transcript_file, "r") as f:
                    transcript = f.read().strip()
                log(f"[{time.time()}] 📝 Transcription result: {transcript}")
                if transcript:
                    speak(f"You said: {transcript}", _config)
            else:
                log(f"[{time.time()}] 🤷 No transcription file produced.")

        except Exception as e:
            log(f"[{time.time()}] ❌ Transcription error: {e}")
        finally:
            _job_queue.task_done()
