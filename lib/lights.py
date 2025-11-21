import time
from rainbowio import colorwheel
from neopixel import NeoPixel

RED = (255, 0, 0)
ORANGE = (255, 50, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
PINK = (255, 75, 150)
WHITE = (255, 255, 255)
NOTHING = (0, 0, 0)

class Lights():
    def __init__(self, pin, num_pixels):
        self.pixels = NeoPixel(pin, num_pixels, brightness=0.1, auto_write=False)
        self.num_pixels = num_pixels
        self.hue_offset = 0

    def rainbow_cycle(self, wait):
        for j in range(255):
            for i in range(self.num_pixels):
                rc_index = (i * 256 // self.num_pixels) + j
                self.pixels[i] = colorwheel(rc_index & 255)
            self.pixels.show()
            time.sleep(wait)

    def show_colour(self, color):
        self.pixels.fill(color)
        self.pixels.show()

    def sweeping_clear(self, wait=0.1):
        for i in range(self.num_pixels):
            self.pixels[i] = NOTHING
            self.pixels.show()
            time.sleep(wait)

    def loading_bar(self, wait=0.1):
        for i in range(self.num_pixels):
            self.pixels[self.num_pixels - 1] = WHITE
            self.pixels.show()
            time.sleep(wait)

    def fill_rainbow_to(self, pix):
        for i in range(self.num_pixels - pix, self.num_pixels):
            rc_index = (i * 256 // self.num_pixels) + self.hue_offset
            self.pixels[i] = colorwheel(rc_index & 255)
        self.pixels.show()

