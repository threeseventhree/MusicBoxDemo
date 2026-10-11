from machine import Pin # type: ignore
from time import sleep

class ButtonHandler:
    def __init__(self):
        self.enterButton = Pin(19, Pin.IN, Pin.PULL_UP)
        self.scrollButton = Pin(18, Pin.IN, Pin.PULL_UP)
        self.backButton = Pin(17, Pin.IN, Pin.PULL_UP)
    
    def waitForRelease(self, button):
        while not button.value():
            sleep(0.01)
