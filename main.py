import os
import time
import argparse
import subprocess
from config import load_config
from logger import init_logging, log
from recorder import record_audio, check_microphone_activity, select_input_device, get_device_index_by_name
from speaker import init_tts
from transcriber import start_worker, enqueue_transcription, Say
from hotword import init_hotword, register_callback
from speaker import speak

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
    parser = argparse.ArgumentParser(description="Virgil Voice Assistant")
    parser.add_argument("-d", "--duration", type=int, help="Recording duration in seconds")
    parser.add_argument("-l", "--log", action="store_true", help="Enable logging to file")
    parser.add_argument("--audio-select", action="store_true", help="Force audio selection screen at startup")
    # todo: add a help screen
    # todo: bain on unrecognized arg

    args = parser.parse_args()
    config = load_config(args)

    force_audio_select = args.audio_select if hasattr(args, "audio_select") else False
    config["audio_input_name"] = select_input_device(config["config_path"], force_audio_select)
    config["audio_input"] = get_device_index_by_name(config["audio_input_name"])

    play_sound( "assets/virgil_startup.wav" )

    init_logging(config)

    # ...
    if not check_microphone_activity(config.get("audio_input")):
        Say("Microphone not detected or too quiet. Please check your setup.")
        exit(1)

    register_callback(handle_wake)
    init_hotword(config)

    init_tts(config)
    start_worker(config)

    log(f"[{time.time()}] 🧠 Virgil Voice Assistant is live. Say the wake word...")
    Say("Virgil ready.")

    try:
        while True:
            pass  # Main thread idle while hotword and transcription threads run

    except KeyboardInterrupt:
        log(f"[{time.time()}] 👋 Shutting down...")
