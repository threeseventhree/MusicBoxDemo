from time import time, sleep
import framebuf  # type: ignore
import ubinascii  # type: ignore
from src.display import DisplayHandler


class MenuScreen:
    def __init__(self, displayHandler: DisplayHandler):
        self.displayHandler = displayHandler
        self.cursorPos = 0
        self.options = ["Recognize", "Spotify", "Settings"]

    def show(self):
        self.displayHandler.fill(0)
        self.displayHandler.centerText("MusicBox", 0)
        self.displayHandler.displayParamsList(self.options, self.cursorPos)
        self.displayHandler.show()

    def scroll(self):
        self.cursorPos += 1
        if self.cursorPos >= len(self.options): self.cursorPos = 0
        self.show()

    def enter(self):
        if self.cursorPos == 0:
            self.displayHandler.screen = "recognize"
        elif self.cursorPos == 1:
            self.displayHandler.screen = "spotify"
        elif self.cursorPos == 2:
            self.displayHandler.screen = "settings"


class RecognizeScreen:
    def __init__(self, displayHandler: DisplayHandler):
        self.displayHandler = displayHandler

    def show(self):
        self.displayHandler.display.fill(0)
        self.displayHandler.centerText("Recognize Song", 0)
        self.displayHandler.centerText("Listening...", 24)
        self.displayHandler.display.show()

    def listen(self):
        print("Testing nowPlaying")


class SpotifyScreen:
    def __init__(self, displayHandler: DisplayHandler, spotifyService):
        self.displayHandler = displayHandler
        self.spotifyService = spotifyService
        self.cursorPos = 0
        self.options = ["Now Playing", "Connect", "Disconnect"]
        self.connected = False
        self.nowPlayingActive = False
        self.lastUpdate = 0
        self.updateInterval = 5
        self.artKey = None
        self.artBuffer = None

    def show(self):
        self.nowPlayingActive = False
        self.displayHandler.fill(0)
        self.displayHandler.centerText("Spotify", 0)
        self.displayHandler.displayParamsList(self.options, self.cursorPos)
        self.displayHandler.show()

    def scroll(self):
        if self.nowPlayingActive:
            self.show()
            return
        self.cursorPos += 1
        if self.cursorPos >= len(self.options): self.cursorPos = 0
        self.show()

    def enter(self):
        if self.cursorPos == 0:
            self.nowPlaying()
        elif self.cursorPos == 1:
            self.connect()
        elif self.cursorPos == 2:
            self.disconnect()

    def message(self, line1, line2=None):
        self.displayHandler.fill(0)
        self.displayHandler.centerText("Spotify", 0)
        self.displayHandler.centerText(line1, 24)
        if line2:
            self.displayHandler.centerText(line2, 36)
        self.displayHandler.show()

    def nowPlaying(self):
        if not self.connected:
            self.message("Not Connected")
            return
        self.nowPlayingActive = True
        self.lastUpdate = time()
        self.updateNowPlaying()

    def connect(self):
        self.message("Connecting...")
        try:
            self.spotifyService.connect()
            # Poll the PC until it reports connected (about 60 s, then give up)
            for _ in range(30):
                if self.spotifyService.isConnected():
                    self.connected = True
                    self.message("Connected")
                    return
                sleep(2)
            self.message("Timed out")
        except OSError:
            self.message("No PC link")

    def disconnect(self):
        self.connected = False
        self.nowPlayingActive = False
        self.message("Disconnected")

    def update(self):
        if not self.nowPlayingActive: return
        currentTime = time()
        if currentTime - self.lastUpdate < self.updateInterval: return
        self.lastUpdate = currentTime
        self.updateNowPlaying()

    def updateNowPlaying(self):
        try:
            track = self.spotifyService.getCurrentlyPlaying()
        except OSError:
            self.message("No PC link")
            return

        if not track or "error" in track:
            self.message("Nothing Playing")
            return

        if not track["playing"]:
            self.message("Paused")
            return

        progress = track["progressMs"] // 1000
        duration = track["durationMs"] // 1000
        progressText = "%d:%02d / %d:%02d" % (
            progress // 60, progress % 60, duration // 60, duration % 60
        )

        art = track.get("artwork")
        if art and art != self.artKey:
            data = bytearray(ubinascii.a2b_base64(art))
            self.artBuffer = framebuf.FrameBuffer(data, 32, 32, framebuf.MONO_VLSB)
            self.artKey = art
        elif not art:
            self.artBuffer = None
            self.artKey = None

        self.displayHandler.fill(0)
        self.displayHandler.centerText("Now Playing", 0)

        if self.artBuffer:
            self.displayHandler.blit(self.artBuffer, 0, 20)
            x, width = 36, 11 # text sits to the right of the cover
        else:
            x, width = 0, 16

        self.displayHandler.text(track["title"][:width], x, 20)
        self.displayHandler.text(track["artist"][:width], x, 32)
        if self.artBuffer:
            self.displayHandler.text(track["album"][:width], x, 44)
        self.displayHandler.text(progressText, x if self.artBuffer else 0, 56)
        self.displayHandler.show()


class SettingsScreen:
    def __init__(self, displayHandler: DisplayHandler):
        self.displayHandler = displayHandler
        self.cursorPos = 0
        self.options = ["Information"]

    def show(self):
        self.displayHandler.fill(0)
        self.displayHandler.centerText("Settings", 0)
        self.displayHandler.displayParamsList(self.options, self.cursorPos)
        self.displayHandler.show()

    def scroll(self):
        self.cursorPos += 1
        if self.cursorPos >= len(self.options): self.cursorPos = 0
        self.show()
