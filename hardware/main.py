from time import sleep
from src.buttons import ButtonHandler
from src.display import DisplayHandler
from src.screens import MenuScreen, RecognizeScreen, SpotifyScreen, SettingsScreen

displayHandler = DisplayHandler()
buttonHandler = ButtonHandler()

menuScreen = MenuScreen(displayHandler)
spotifyScreen = SpotifyScreen(displayHandler)
recognizeScreen = RecognizeScreen(displayHandler)
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
        if(displayHandler.screen != "menu"):
            menuScreen.show()
            displayHandler.screen = "menu"
        buttonHandler.waitForRelease(buttonHandler.backButton)

    if displayHandler.screen == "spotify":
        spotifyScreen.update()
