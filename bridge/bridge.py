# pip install pyserial requests
import json
import serial
import requests

PORT = "COM5"
BASE_URL = "https://musicbox-kohl.vercel.app"   # your deployed Next.js app
HTTP_TIMEOUT = 4    # must stay under the ESP32's 5 s wait

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
        return api("GET", f"/api/sessions/{sessionID}/currently-playing")

    return {"error": "not found"}


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
        ser.write(("@RES " + json.dumps(reply) + "\n").encode())
    elif line:
        print("[esp32]", line)
