import time
import os
import json
from dotenv import load_dotenv

CONFIG_DEFAULTS = {
    "default_duration": 3,
    "transcript_log": "virgil.log",
    "tts_model": "tts_models/en/ljspeech/tacotron2-DDC",
    "whisper_dir": os.path.expanduser("~/virgil/whisper.cpp"),
    "audio_input": "input.wav",
    "audio_output": "out.wav",
    "wake_word_model": os.path.expanduser("~/virgil/assets/virgil.ppn"),
    "porcupine_access_key": ""
}

def load_config(cli_args):
    # Load .env if it exists
    load_dotenv()

    # Load config.json if it exists
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    file_config = {}
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            file_config = json.load(f)

    config = CONFIG_DEFAULTS.copy()
    config.update(file_config)

    # Environment variable overrides
    config["tts_model"] = os.getenv("TTS_MODEL", config["tts_model"])
    config["log_enabled"] = os.getenv("LOGGING", "false").lower() == "true"
    config["wake_word_model"] = os.getenv("WAKE_WORD_MODEL", config["wake_word_model"])
    config["porcupine_access_key"] = os.getenv("PORCUPINE_ACCESS_KEY", config["porcupine_access_key"])

    # CLI overrides
    if cli_args.duration:
        config["default_duration"] = cli_args.duration
    if cli_args.log:
        config["log_enabled"] = True

    # Derived paths
    config["whisper_bin"] = os.path.join(config["whisper_dir"], "build/bin/whisper-cli")
    config["whisper_model"] = os.path.join(config["whisper_dir"], "models/ggml-base.en.bin")
    config["transcription_file"] = os.path.join(config["whisper_dir"], "transcription.txt")

    return config
