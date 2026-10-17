"""Settings for the bridge. Values come from the .env file in the repo root
(or from real environment variables, which win if both exist)."""
import os
import re
from pathlib import Path

KNOWN_KEYS = {"MUSICBOX_API_URL", "SERIAL_PORT", "RECOGNIZER_PYTHON", "OPEN_LOGIN_IN_BROWSER"}


def cleanValue(value):
    value = value.strip()
    quoted = re.fullmatch(r"[rR]?([\"'])(.*)\1", value)     # "text", 'text' (and r"text" by mistake)
    return quoted.group(2) if quoted else value


def loadEnv(path):
    values = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            if key not in KNOWN_KEYS:
                print(f"warning: unknown key '{key}' in .env (known keys: {', '.join(sorted(KNOWN_KEYS))})")
            values[key] = cleanValue(value)
    return values


_file = loadEnv(Path(__file__).resolve().parent.parent / ".env")


def get(name, default=None):
    return os.environ.get(name) or _file.get(name) or default


BASE_URL = get("MUSICBOX_API_URL")
if not BASE_URL:
    raise SystemExit("MUSICBOX_API_URL is missing. Copy .env.example to .env and fill it in.")

PORT = get("SERIAL_PORT", "COM5")

# Open the Spotify login page in the PC's browser when Connect is pressed on the box
OPEN_LOGIN_IN_BROWSER = get("OPEN_LOGIN_IN_BROWSER", "true").lower() not in ("0", "false", "no", "off")

RECOGNIZER_PYTHON = get("RECOGNIZER_PYTHON")     # None = use the bridge's own Python
if RECOGNIZER_PYTHON and not Path(RECOGNIZER_PYTHON).exists():
    raise SystemExit(f"RECOGNIZER_PYTHON points to a file that doesn't exist: {RECOGNIZER_PYTHON}")
