from machine import Pin, I2C  # type: ignore
import sh1106
import ssd1306


class DisplayHandler:
    """Drawing helpers around any display driver (SH1106, SSD1306 ...) that has
    the usual framebuf API. Pass in an already-created driver object."""

    def __init__(self, display, width=128, height=64):
        self.width = width
        self.height = height
        self.fontSize = 8
        self.yOffset = 8
        self.display = display
        self.screens = ["recognize", "spotify", "settings"]
        self.screen = "menu"

    def centerText(self, text: str, y: int):
        length = len(text)
        lengthPixels = self.fontSize * length
        centerXPos = int(self.width / 2)
        x = centerXPos - int(lengthPixels / 2)
        self.display.text(text, x, y)

    def displayParamsList(self, params: list, cursorPos: int):
        for i, item in enumerate(params):
            y = self.yOffset * 2 + i * self.fontSize
            if i == cursorPos:
                self.display.text("> " + item, 0, y)
            else:
                self.display.text("  " + item, 0, y)

    def show(self):
        self.display.show()

    def fill(self, color):
        self.display.fill(color)

    def fillRect(self, x, y, width, height, color):
        self.display.fill_rect(x, y, width, height, color)

    def text(self, text: str, x: int, y: int):
        self.display.text(text, x, y, 1)

    def blit(self, bitmap, x, y):
        self.display.blit(bitmap, x, y)

    def powerOn(self):
        self.display.poweron()

    def powerOff(self):
        self.display.poweroff()


def createTextDisplay():
    """Main screen: SH1106 on I2C bus 0 (SDA 21, SCL 22)."""
    i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
    return DisplayHandler(sh1106.SH1106_I2C(128, 64, i2c, rotate=180))


def createCoverDisplay():
    """Cover screen: SSD1306 on I2C bus 1 (SCL 25, SDA 26)."""
    i2c = I2C(1, scl=Pin(25), sda=Pin(26), freq=400000)
    display = ssd1306.SSD1306_I2C(128, 64, i2c)
    # If the cover appears upside down, uncomment the next line:
    # display.rotate(False)
    return DisplayHandler(display)
