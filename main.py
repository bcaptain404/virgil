import time
import argparse
#import os
from config import load_config
from logger import init_logging, log
from recorder import record_audio
from speaker import init_tts
from transcriber import start_worker, enqueue_transcription
from hotword import init_hotword, register_callback

def handle_wake():
    log(f"[{time.time()}] 🎤 Wake word detected. Starting recording...")
    record_audio(config["audio_input"], config["default_duration"])
    enqueue_transcription(config["audio_input"])

if __name__ == "__main__":
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
