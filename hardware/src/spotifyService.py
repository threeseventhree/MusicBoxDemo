class SpotifyService:
    def __init__(self, client):
        self.client = client

    def connect(self):
        return self.client.get("/spotify/connect")

    def isConnected(self):
        return self.client.get("/spotify/status")["connected"]

    def getCurrentlyPlaying(self):
        return self.client.get("/spotify/currently-playing")

    def getArtwork(self):
        return self.client.get("/spotify/artwork")
