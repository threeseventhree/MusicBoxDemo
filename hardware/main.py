from src.microphone import Microphone
from src.buttons import ButtonHandler
from src.display import createTextDisplay, createCoverDisplay
from src.screens import MenuScreen, RecognizeScreen, SpotifyScreen, SettingsScreen
from src.serialClient import SerialClient
from src.spotifyService import SpotifyService

microphone = Microphone()
displayHandler = createTextDisplay()
coverDisplay = createCoverDisplay()
buttonHandler = ButtonHandler()

client = SerialClient(timeout=10)
spotifyService = SpotifyService(client)

menuScreen = MenuScreen(displayHandler)
spotifyScreen = SpotifyScreen(displayHandler, coverDisplay, spotifyService)
recognizeScreen = RecognizeScreen(displayHandler, coverDisplay, microphone, client)
settingsScreen = SettingsScreen(displayHandler)

menuScreen.show()
while True:
    if not buttonHandler.enterButton.value():
        if displayHandler.screen == "menu":
            menuScreen.enter()
            if displayHandler.screen == "recognize":
                recognizeScreen.show()
            elif displayHandler.screen == "spotify":
                spotifyScreen.show()
            elif displayHandler.screen == "settings":
                settingsScreen.show()
        elif displayHandler.screen == "spotify":
            spotifyScreen.enter()
        elif displayHandler.screen == "recognize":
            recognizeScreen.enter()
        buttonHandler.waitForRelease(buttonHandler.enterButton)

    if not buttonHandler.scrollButton.value():
        if displayHandler.screen == "menu":
            menuScreen.scroll()
        elif displayHandler.screen == "spotify":
            spotifyScreen.scroll()
        elif displayHandler.screen == "settings":
            settingsScreen.scroll()
        buttonHandler.waitForRelease(buttonHandler.scrollButton)

    if not buttonHandler.backButton.value():
        if displayHandler.screen != "menu":
            if displayHandler.screen == "spotify":
                spotifyScreen.leave()
            elif displayHandler.screen == "recognize":
                recognizeScreen.leave()
            menuScreen.show()
            displayHandler.screen = "menu"
        buttonHandler.waitForRelease(buttonHandler.backButton)

    if displayHandler.screen == "spotify":
        spotifyScreen.update()
