import sys
import json
import time
import select


class SerialClient:
    """Same get()/post() interface a Wi-Fi client would have, but the request
    goes over USB to bridge.py on the PC and the reply comes back the same way."""

    def __init__(self, timeout=5):
        self.timeout = timeout
        self.poll = select.poll() # type: ignore
        self.poll.register(sys.stdin, select.POLLIN) # type: ignore

    def get(self, address):
        return self._request("GET", address, None)

    def post(self, address, data=None):
        return self._request("POST", address, data)

    def _request(self, method, address, data):
        # Throw away anything left over from an earlier, timed-out request
        while self.poll.poll(0):
            sys.stdin.read(1)

        sys.stdout.write("@REQ " + json.dumps({"m": method, "p": address, "d": data}) + "\n")

        buf = ""
        start = time.ticks_ms() # type: ignore
        while time.ticks_diff(time.ticks_ms(), start) < self.timeout * 1000: # type: ignore
            if self.poll.poll(50):
                ch = sys.stdin.read(1)
                if ch == "\n":
                    if buf.startswith("@RES "):
                        return json.loads(buf[5:])
                    buf = ""
                else:
                    buf += ch
        raise OSError("no reply from PC")
