import sys
import json
import time
import select

class SerialClient:
    def __init__(self, timeout=5):
        self.timeout = timeout
        self.poll = select.poll() #type: ignore
        self.poll.register(sys.stdin, select.POLLIN) #type: ignore

    def get(self, address):
        return self._request("GET", address, None)

    def post(self, address, data=None):
        return self._request("POST", address, data)

    def sendAudio(self, data, rate):
        self._flush()
        sys.stdout.write("@AUDIO %d %d\n" % (len(data), rate))
        out = sys.stdout.buffer
        view = memoryview(data)
        for i in range(0, len(data), 512):
            out.write(view[i:i + 512])
        return self._readReply(30)

    def _flush(self):
        while self.poll.poll(0):
            sys.stdin.read(1)

    def _request(self, method, address, data):
        self._flush()
        sys.stdout.write("@REQ " + json.dumps({"m": method, "p": address, "d": data}) + "\n")
        return self._readReply()

    def _readReply(self, timeout=None):
        timeout = timeout or self.timeout
        buf = ""
        start = time.ticks_ms() #type: ignore
        while time.ticks_diff(time.ticks_ms(), start) < timeout * 1000: #type: ignore
            if self.poll.poll(50):
                ch = sys.stdin.read(1)
                if ch == "\n":
                    if buf.startswith("@RES "):
                        return json.loads(buf[5:])
                    buf = ""
                else:
                    buf += ch
        raise OSError("no reply from PC")
