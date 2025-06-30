import os
import time
import argparse
import subprocess
from config import load_config
from logger import init_logging, log
from recorder import record_audio
from speaker import init_tts
from transcriber import start_worker, enqueue_transcription
from hotword import init_hotword, register_callback

def play_sound( sound_file ):
    if os.path.exists(sound_file):
        try:
            subprocess.Popen(
                ["ffplay", "-nodisp", "-autoexit", sound_file],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            log(f"[{time.time()}] 🔊 Played startup sound.")
        except Exception as e:
            log(f"[{time.time()}] ⚠️ Failed to play startup sound: {e}")
    else:
        log(f"[{time.time()}] ⚠️ Startup sound file not found.")

def handle_wake():
    log(f"[{time.time()}] 🎤 Wake word detected. Starting recording...")
    record_audio(config["audio_input"], config["default_duration"])
    enqueue_transcription(config["audio_input"])

if __name__ == "__main__":
    play_sound( "assets/virgil_startup.wav" )

    parser = argparse.ArgumentParser(description="Virgil Voice Assistant")
    parser.add_argument("-d", "--duration", type=int, help="Recording duration in seconds")
    parser.add_argument("-l", "--log", action="store_true", help="Enable logging to file")

    args = parser.parse_args()
    config = load_config(args)

    init_logging(config)
    init_tts(config)
    start_worker(config)
    register_callback(handle_wake)
    init_hotword(config)

    log(f"[{time.time()}] 🧠 Virgil Voice Assistant is live. Say the wake word...")

    try:
        while True:
            pass  # Main thread idle while hotword and transcription threads run

    except KeyboardInterrupt:
        log(f"[{time.time()}] 👋 Shutting down...")
