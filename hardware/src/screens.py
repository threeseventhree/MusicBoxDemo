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

from src.display import DisplayHandler
from time import time

class SpotifyScreen:
    def __init__(self, displayHandler: DisplayHandler):
        self.displayHandler = displayHandler
        self.cursorPos = 0
        self.options = ["Now Playing", "Connect", "Disconnect"]
        self.connected = False
        self.nowPlayingActive = False
        self.lastUpdate = 0
        self.updateInterval = 5

    def show(self):
        self.displayHandler.fill(0)
        self.displayHandler.centerText("Spotify", 0)
        self.displayHandler.displayParamsList(self.options, self.cursorPos)
        self.displayHandler.show()

    def scroll(self):
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

    def nowPlaying(self):
        if not self.connected:
            self.displayHandler.fill(0)
            self.displayHandler.centerText("Spotify", 0)
            self.displayHandler.centerText("Not Connected", 24)
            self.displayHandler.show()
            return
        self.nowPlayingActive = True
        self.lastUpdate = 0
        self.updateNowPlaying()

    def connect(self):
        self.displayHandler.fill(0)
        self.displayHandler.centerText("Connecting...", 24)
        self.displayHandler.show()

    def disconnect(self):
        self.connected = False
        self.nowPlayingActive = False

        self.displayHandler.fill(0)
        self.displayHandler.centerText("Spotify", 0)
        self.displayHandler.centerText("Disconnected", 24)
        self.displayHandler.show()

    def update(self):
        if not self.nowPlayingActive: return
        currentTime = time()
        if currentTime - self.lastUpdate < self.updateInterval: return
        self.lastUpdate = currentTime
        self.updateNowPlaying()

    def updateNowPlaying(self):
        track = None
        if not track:
            self.displayHandler.fill(0)
            self.displayHandler.centerText("Now Playing",0)
            self.displayHandler.centerText("Nothing Playing",24)
            self.displayHandler.show()
            return

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
