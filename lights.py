import time
import random

from rainbowio import colorwheel
from neopixel import NeoPixel
from utils import colour_interp, palette_interp, scale_tuple

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

sunrise_palette = [YELLOW, ORANGE, RED, BLUE, BLUE, BLUE]

demo_duration = 5

class Lights():
    def __init__(self, pin, num_pixels):
        self.pixels = NeoPixel(pin, num_pixels, brightness=0.1, auto_write=False)
        self.num_pixels = num_pixels
        self.hue_offset = 0
        self.sparkle_lifetime = 5
        self.sparkles = [(20, 1)]
        self.fired_sunrise = 0

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

    def fill_rainbow_to(self, percentage):
        pix = percentage * self.num_pixels // 1
        for i in range(self.num_pixels - pix, self.num_pixels):
            rc_index = (i * 256 // self.num_pixels) + self.hue_offset
            self.pixels[i] = colorwheel(rc_index & 255)
        self.pixels.show()

    def bump_rainbow(self, calmness):
        for i in range(self.num_pixels):
            rc_index = (i * 256 // self.num_pixels) + self.hue_offset // calmness
            self.pixels[i] = colorwheel(rc_index & 255)
        self.pixels.show()
        self.hue_offset += 1

    def bump_white_over_rainbow(self, calmness, white_chaser_size=5):
        for i in range(self.num_pixels):
            rc_index = (i * 256 // self.num_pixels) + (self.hue_offset // calmness)
            self.pixels[i] = colorwheel(rc_index & 255)
        for i in range(white_chaser_size):
            self.pixels[(self.hue_offset // (calmness * 5) + i) % self.num_pixels] = WHITE
        self.pixels.show()
        self.hue_offset += 1

    def bump_fade_colours(self, palette, chill):
        p = len(palette)
        for i in range(self.num_pixels // p):
            for k in range(p):
                self.pixels[(i + (self.hue_offset // chill) + (k * self.num_pixels // p)) % self.num_pixels] = colour_interp(palette[k], palette[(k + 1) % p], i * p / self.num_pixels)
            self.pixels.show()
        self.hue_offset += 1

    def fade_colours(self, palette):
        p = len(palette)
        for j in range(0, self.num_pixels):
            for i in range(self.num_pixels // p):
                for k in range(p):
                    self.pixels[(i + j + (k * self.num_pixels // p)) % self.num_pixels] = colour_interp(palette[k], palette[(k + 1) % p], i * p / self.num_pixels)
                self.pixels.show()

    def chaser(self, palette, chaser_size, wait):
        p = len(palette)
        for j in range(self.num_pixels):
            for i in range(self.num_pixels):
                self.pixels[(i + j) % self.num_pixels] = palette[(i // chaser_size) % p]
            self.pixels.show()
            time.sleep(wait)

    def pong(self, colour, wait):
        for i in range(self.num_pixels):
            self.pixels.fill(NOTHING)
            self.pixels[i] = colour
            self.pixels.show()
            time.sleep(wait)

    # helper for avoiding index out of range
    def set_colour(self, i, colour):
        if i >= 0 and i < self.num_pixels:
            self.pixels[i] = colour

    def sunrise(self):
        palette = [YELLOW, ORANGE, RED, BLUE]
        for i in range(self.num_pixels):
            self.pixels[i] = palette_interp(palette, i / self.num_pixels)
        self.pixels.show()

    def bump_chaser(self, palette, wait, frame, tail=0):
        colour = palette_interp(palette, (frame % self.num_pixels) / self.num_pixels)
        if frame < self.num_pixels:
            self.pixels[frame] = colour
        for i in range(1, tail):
            if frame - i >= 0 and frame - i < self.num_pixels:
                self.pixels[frame - i] = scale_tuple(self.pixels[frame - i], 2 / tail)
        # clean cutoff for tail:
        self.pixels[(frame - tail + self.num_pixels) % self.num_pixels] = NOTHING
        self.pixels.show()
        time.sleep(wait)

    def bump_repeat_chaser(self, palette, wait, tail):
        self.frame = (self.frame + 1) % self.num_pixels
        self.bump_chaser(palette, wait, self.frame, tail)

    def bump_onetime_chaser(self, palette, wait, tail):
        self.frame += 1
        self.bump_chaser(palette, wait, self.frame, tail)

    def bump_sunrise(self, wait):
        self.bump_onetime_chaser(sunrise_palette, wait, 5)

    def bump_second_sunrise(self, wait):
        if self.fired_sunrise < 1:
            self.frame = -1
            self.fired_sunrise = 1
        self.bump_onetime_chaser(sunrise_palette, wait, 5)

    def bump_third_sunrise(self, wait):
        if self.fired_sunrise < 2:
            self.frame = -1
            self.fired_sunrise = 2
        self.bump_onetime_chaser(sunrise_palette, wait, 10)

    def draw_sparkles(self, wait):
        self.pixels.fill(NOTHING)
        result = []
        for (location, size) in self.sparkles:
            brightness = scale_tuple(WHITE, 1 / (size * size))
            for i in range(location - size, location + size + 1):
                self.set_colour(i, brightness)
            if size < self.sparkle_lifetime:
                result.append((location, size + 1))
        self.sparkles = result
        self.pixels.show()
        time.sleep(wait)

    def bump_sparkles(self, wait):
        if random.random() < 0.3:
            location = random.randrange(self.num_pixels)
            self.sparkles.append((location, 1))
        self.draw_sparkles(wait)

    def reset(self):
        self.show_colour(NOTHING)

    def meadow(self):
        for _ in range(demo_duration):
            self.fade_colours([YELLOW, GREEN, CYAN, (0, 255, 50)])
        self.reset()

    def bump_trans_pride(self):
        self.bump_chaser([PINK, CYAN, WHITE], 5, 0.05)

    def sunset(self):
        for _ in range(demo_duration):
            self.fade_colours([ORANGE, PURPLE, BLUE])
        self.reset()

    def glitter(self):
        for _ in range(3):
            self.chaser([WHITE, NOTHING, NOTHING, PURPLE, NOTHING, NOTHING, WHITE, NOTHING, ORANGE, NOTHING], 3, 0.1)
        self.reset()

    def glow(self):
        for _ in range(demo_duration):
            self.fade_colours([RED, ORANGE, YELLOW])
        self.reset()
