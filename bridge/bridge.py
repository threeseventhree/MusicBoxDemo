# pip install pyserial requests
import json
import time
import traceback
import hashlib
import serial #type: ignore
import requests #type: ignore
from artwork import getArtwork
from audio import saveWav, toRecognitionWav
from recognize import recognizeSafely
from config import BASE_URL, PORT, RECOGNIZER_PYTHON
HTTP_TIMEOUT = 4
CHUNK = 32
CHUNK_DELAY = 0.02

sessionID = None
latestArtURL = None

def artID(url):
    return hashlib.md5(url.encode()).hexdigest()[:8]

def api(method, path):
    r = requests.request(method, BASE_URL + path, timeout=HTTP_TIMEOUT)
    r.raise_for_status()
    return r.json()

def handle(path):
    global sessionID, latestArtURL
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
        latestArtURL = track.pop("artworkURL", None)
        if latestArtURL:
            track["artID"] = artID(latestArtURL)
        return track

    if path in ("/spotify/artwork", "/artwork"):
        if not latestArtURL:
            return {"error": "no artwork"}
        return {"id": artID(latestArtURL), "art": getArtwork(latestArtURL, 64)}

    return {"error": "not found"}

def readExact(n, limit=20):
    data = bytearray()
    deadline = time.time() + limit
    while len(data) < n and time.time() < deadline:
        data += ser.read(n - len(data))
    return bytes(data)

def identify(samples, rate):
    global latestArtURL
    path = toRecognitionWav(samples, rate)
    result = recognizeSafely(path, RECOGNIZER_PYTHON)
    if not result["match"]:
        print("  shazam: no match")
        return {"match": False}
    print("  shazam:", result["artist"], "-", result["title"])
    latestArtURL = result.pop("coverURL", None)
    if latestArtURL:
        result["artID"] = artID(latestArtURL)
    return result

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
ser.timeout = 1
ser.dtr = False
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
    elif line.startswith("@AUDIO "):
        try:
            _, count, rate = line.split()
            count, rate = int(count), int(rate)
            samples = readExact(count)
            if len(samples) < count:
                reply = {"error": f"audio incomplete: {len(samples)} of {count} bytes"}
            else:
                print("audio:", saveWav(samples, rate))
                reply = identify(samples, rate)
        except Exception as e:
            traceback.print_exc()
            print("  error:", e)
            reply = {"error": str(e)}
        send("@RES " + json.dumps(reply) + "\n")
    elif line:
        print("[esp32]", line)
