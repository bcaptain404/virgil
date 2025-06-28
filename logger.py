import time
import os
import time

LOG_FILE = "virgil.log"
OLD_LOG_FILE = "virgil.log.old"

_log_enabled = False
_log_path = None

def init_logging(config):
    global _log_enabled, _log_path
    _log_enabled = config.get("log_enabled", False)
    _log_path = config.get("transcript_log", LOG_FILE)

    if os.path.exists(_log_path):
        if os.path.exists(OLD_LOG_FILE):
            os.remove(OLD_LOG_FILE)
        os.rename(_log_path, OLD_LOG_FILE)

    with open(_log_path, "w") as f:
        f.write("")  # create empty log

def log(message):
    if not _log_enabled:
        return
    timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
    with open(_log_path, "a") as f:
        f.write(f"{timestamp} {message}\n")
    print(message)
