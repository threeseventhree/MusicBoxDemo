import os
from pathlib import Path
def loadEnv(path):
    values = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip('"').strip("'")
    return values
_file = loadEnv(Path(__file__).resolve().parent.parent / ".env")

def get(name, default=None):
    return os.environ.get(name) or _file.get(name) or default
BASE_URL = get("MUSICBOX_API_URL")
if not BASE_URL:
    raise SystemExit("MUSICBOX_API_URL is missing. Copy .env.example to .env and fill it in.")
PORT = get("SERIAL_PORT", "COM5")
RECOGNIZER_PYTHON = get("RECOGNIZER_PYTHON")
