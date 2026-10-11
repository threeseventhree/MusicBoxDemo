# pip install pyserial requests
import json
import time
import serial
import requests
from artwork import getArtwork

PORT = "COM5"
BASE_URL = "https://musicbox-kohl.vercel.app"   # your deployed Next.js app
HTTP_TIMEOUT = 4    # keep requests short so replies come back quickly
CHUNK = 32          # the ESP32's serial input buffer is small, so send replies in pieces
CHUNK_DELAY = 0.02

sessionID = None


def api(method, path):
    r = requests.request(method, BASE_URL + path, timeout=HTTP_TIMEOUT)
    r.raise_for_status()
    return r.json()


def handle(path):
    global sessionID

    if path == "/spotify/connect":
        sessionID = api("POST", "/api/sessions")["sessionID"]
        url = f"{BASE_URL}/connect/{sessionID}"
        print("Open this on your phone/PC to log in to Spotify:\n ", url)
        return {"session_id": sessionID, "url": url}

    if path == "/spotify/status":
        if not sessionID:
            return {"connected": False}
        return {"connected": api("GET", f"/api/sessions/{sessionID}")["connected"]}

    if path == "/spotify/currently-playing":
        if not sessionID:
            return None
        track = api("GET", f"/api/sessions/{sessionID}/currently-playing")
        url = track.pop("artworkURL", None)
        if track.get("playing") and url:
            try:
                track["artwork"] = getArtwork(url)
            except Exception as e:
                print("  artwork failed:", e)    # still send the track without a cover
        return track

    return {"error": "not found"}


def send(text):
    data = text.encode()
    print("  reply:", len(data), "bytes")
    for i in range(0, len(data), CHUNK):
        ser.write(data[i:i + CHUNK])
        ser.flush()
        time.sleep(CHUNK_DELAY)


ser = serial.Serial()
ser.port = PORT
ser.baudrate = 115200
ser.timeout = 1      # so Ctrl-C works while waiting
ser.dtr = False      # stops the ESP32 resetting when the port opens
ser.rts = False
ser.open()
print("bridge running on", PORT, "(Ctrl-C to stop)")

while True:
    line = ser.readline().decode(errors="ignore").strip()
    if line.startswith("@REQ "):
        try:
            req = json.loads(line[5:])
            print("request:", req["m"], req["p"])
            reply = handle(req["p"])
        except Exception as e:
            print("  error:", e)
            reply = {"error": str(e)}
        send("@RES " + json.dumps(reply) + "\n")
    elif line:
        print("[esp32]", line)
