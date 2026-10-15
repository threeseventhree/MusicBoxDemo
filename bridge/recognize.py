# pip install shazamio
import asyncio
import json
import subprocess
import sys
from pathlib import Path

def parseTrack(result):
    track = (result or {}).get("track")
    if not track:
        return {"match": False}

    album = ""
    for section in track.get("sections", []):
        for item in section.get("metadata", []) or []:
            if item.get("title", "").lower() == "album":
                album = item.get("text", "")

    images = track.get("images", {}) or {}
    return {
        "match": True,
        "title": track.get("title", ""),
        "artist": track.get("subtitle", ""),
        "album": album,
        "coverURL": images.get("coverarthq") or images.get("coverart"),
    }

def recognizeFile(path):
    from shazamio import Shazam
    shazam = Shazam()
    method = getattr(shazam, "recognize", None) or getattr(shazam, "recognize_song")
    return parseTrack(asyncio.run(method(path)))

def recognizeSafely(path, python=None, timeout=25):
    proc = subprocess.run(
        [python or sys.executable, str(Path(__file__).resolve()), str(path)],
        capture_output=True, text=True, timeout=timeout,
    )
    lines = proc.stdout.strip().splitlines()
    if proc.returncode != 0 or not lines:
        tail = " | ".join((proc.stderr or "").strip().splitlines()[-3:])
        raise RuntimeError(f"recognizer failed (exit code {proc.returncode}): {tail}")
    return json.loads(lines[-1])

if __name__ == "__main__":
    print(json.dumps(recognizeFile(sys.argv[1])))
