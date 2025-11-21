import time
import random
import board
import keypad

from audioio import AudioOut
from audiomp3 import MP3Decoder
from audiobusio import I2SOut

from rainbowio import colorwheel
from neopixel import NeoPixel
from adafruit_dotstar import DotStar

print("letsgooo")

pixels = NeoPixel(board.NEOPIXEL, 2, brightness=0.1, auto_write=False)

num_pixels = 59 # 118 # Actually 118 pixels in the strip, but doubled up
dots = DotStar(board.SCK, board.MOSI, num_pixels, brightness=0.2, auto_write=False)

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

def rainbow_cycle(wait):
    for j in range(255):
        pixels.fill(colorwheel(j))
        pixels.show()
        for i in range(num_pixels):
            rc_index = (i * 256 // num_pixels) + j
            dots[i] = colorwheel(rc_index & 255)
        dots.show()
        time.sleep(wait)

def show_colour(color):
    pixels.fill(color)
    pixels.show()
    dots.fill(color)
    dots.show()

def sweeping_clear(wait):
    for i in range(num_pixels):
        dots[i] = NOTHING
        dots.show()
        time.sleep(wait)

def loading_bar(wait):
    for i in range(num_pixels):
        dots[num_pixels - 1] = WHITE
        dots.show()
        time.sleep(wait)

rainbow_cycle(0)  # Increase the number to slow down the rainbow

def fill_rainbow_to(pix):
    for i in range(num_pixels - pix, num_pixels):
        rc_index = (i * 256 // num_pixels) + hue_offset
        dots[i] = colorwheel(rc_index & 255)
    dots.show()

hue_offset = 0
white_chaser_size = 5
frame = 0
fired_sunrise = 0

def bump_rainbow(calmness):
    global hue_offset
    for i in range(num_pixels):
        rc_index = (i * 256 // num_pixels) + hue_offset // calmness
        dots[i] = colorwheel(rc_index & 255)
    dots.show()
    hue_offset += 1

def bump_white_over_rainbow(calmness):
    global hue_offset
    for i in range(num_pixels):
        rc_index = (i * 256 // num_pixels) + (hue_offset // calmness)
        dots[i] = colorwheel(rc_index & 255)
    for i in range(white_chaser_size):
        dots[(hue_offset // (calmness * 5) + i) % num_pixels] = WHITE
    dots.show()
    hue_offset += 1

def lerp(a, b, x):
    return a + (b - a) * x;

def colour_interp(col1, col2, x):
    (r1, g1, b1) = col1
    (r2, g2, b2) = col2
    return (lerp(r1, r2, x), lerp(g1, g2, x), lerp(b1, b2, x))

def bump_fade_colours(palette, chill):
    global hue_offset
    p = len(palette)
    for i in range(num_pixels // p):
        for k in range(p):
            dots[(i + (hue_offset // chill) + (k * num_pixels // p)) % num_pixels] = colour_interp(palette[k], palette[(k + 1) % p], i * p / num_pixels)
        dots.show()
    hue_offset += 1

def fade_colours(palette):
    p = len(palette)
    for j in range(0, num_pixels):
        for i in range(num_pixels // p):
            for k in range(p):
                dots[(i + j + (k * num_pixels // p)) % num_pixels] = colour_interp(palette[k], palette[(k + 1) % p], i * p / num_pixels)
            dots.show()

def chaser(palette, chaser_size, wait):
    p = len(palette)
    for j in range(num_pixels):
        for i in range(num_pixels):
            dots[(i + j) % num_pixels] = palette[(i // chaser_size) % p]
        dots.show()
        time.sleep(wait)

def pong(colour, wait):
    for i in range(num_pixels):
        dots.fill(NOTHING)
        dots[i] = colour
        dots.show()
        time.sleep(wait)

def scale_tuple(t, x):
    return tuple(x * tt for tt in t)

def palette_interp(palette, x):
    p = len(palette) - 1
    col = int(p * x)
    return colour_interp(palette[col], palette[col + 1], (x - col / p) * p)

# helper for avoiding index out of range
def set_colour(i, colour):
    if i >= 0 and i < num_pixels:
        dots[i] = colour

def sunrise():
    palette = [YELLOW, ORANGE, RED, BLUE]
    for i in range(num_pixels):
        dots[i] = palette_interp(palette, i / num_pixels)
    dots.show()

def bump_chaser(palette, wait, frame, tail):
    colour = palette_interp(palette, (frame % num_pixels) / num_pixels)
    if frame < num_pixels:
        dots[frame] = colour
    for i in range(1, tail):
        if frame - i >= 0 and frame - i < num_pixels:
            dots[frame - i] = scale_tuple(dots[frame - i], 2 / tail)
    # clean cutoff for tail:
    dots[(frame - tail + num_pixels) % num_pixels] = NOTHING
    dots.show()
    time.sleep(wait)

def bump_repeat_chaser(palette, wait, tail):
    global frame
    frame = (frame + 1) % num_pixels
    bump_chaser(palette, wait, frame, tail)

def bump_onetime_chaser(palette, wait, tail):
    global frame
    frame += 1
    bump_chaser(palette, wait, frame, tail)

sunrise_palette = [YELLOW, ORANGE, RED, BLUE, BLUE, BLUE]

def bump_sunrise(wait):
    bump_onetime_chaser(sunrise_palette, wait, 5)

def bump_second_sunrise(wait):
    global frame
    global fired_sunrise
    if fired_sunrise < 1:
        frame = -1
        fired_sunrise = 1
    bump_onetime_chaser(sunrise_palette, wait, 5)

def bump_third_sunrise(wait):
    global frame
    global fired_sunrise
    if fired_sunrise < 2:
        frame = -1
        fired_sunrise = 2
    bump_onetime_chaser(sunrise_palette, wait, 10)

sparkle_lifetime = 5
sparkles = [(20, 1)]
def draw_sparkles(wait):
    dots.fill(NOTHING)
    global sparkles
    result = []
    for (location, size) in sparkles:
        brightness = scale_tuple(WHITE, 1 / (size * size))
        for i in range(location - size, location + size + 1):
            set_colour(i, brightness)
        if size < sparkle_lifetime:
            result.append((location, size + 1))
    sparkles = result
    dots.show()
    time.sleep(wait)

def bump_sparkles(wait):
    if random.random() < 0.3:
        location = random.randrange(num_pixels)
        sparkles.append((location, 1))
    draw_sparkles(wait)

def reset():
    show_colour(NOTHING)

demo_duration = 5

def meadow():
    for i in range(demo_duration):
        fade_colours([YELLOW, GREEN, CYAN, (0, 255, 50)])
    reset()

def trans_pride():
    for i in range(demo_duration):
        chaser([PINK, CYAN, WHITE], 5, 0.05)
    reset()

def sunset():
    for i in range(demo_duration):
        fade_colours([ORANGE, PURPLE, BLUE])
    reset()

def glitter():
    for i in range(3):
        chaser([WHITE, NOTHING, NOTHING, PURPLE, NOTHING, NOTHING, WHITE, NOTHING, ORANGE, NOTHING], 3, 0.1)
    reset()

def glow():
    for i in range(demo_duration):
        fade_colours([RED, ORANGE, YELLOW])
    reset()

keys = keypad.Keys((board.A0, board.A1, board.A2,board.A3,board.A4, board.A5), value_when_pressed=False, pull=True)

mp3_file = open("RGSS.mp3", "rb")
decoder = MP3Decoder(mp3_file)
audio = I2SOut(board.D1, board.D10, board.D11)

def play_song():
    print("Playing song...")
    decoder.file = open("RGSS.mp3", "rb")
    audio.play(decoder)
    time_start = time.monotonic()
    while audio.playing:
        current_time = time.monotonic()
        if current_time - time_start < 8.475:
            # first synth stab
            bump_sunrise(0.1)
        elif current_time - time_start < 12.379:
            # second synth stab
            bump_second_sunrise(0.05)
        elif current_time - time_start < 16.683:
            # third synth stab
            bump_third_sunrise(0.05)
        elif current_time - time_start < 20.721:
            # rgss
            bump_sparkles(0.2)
        elif current_time - time_start < 28.574:
            # rgss
            bump_sparkles(0.1)
        elif current_time - time_start < 33.322:
            # RGSS
            bump_sparkles(0.05)
        elif current_time - time_start < 50.005:
            # second singer
            bump_fade_colours([ORANGE, PURPLE, BLUE], 3)
        elif current_time - time_start < 58.302:
            bump_fade_colours([YELLOW, GREEN, CYAN, (0, 255, 50)], 2)
        elif current_time - time_start < 65.268:
            bump_fade_colours([PINK, CYAN], 3)
        elif current_time - time_start < 66.821:
            # big solo
            bump_fade_colours([PINK, CYAN, WHITE], 5)
        elif current_time - time_start < 72.766:
            # choir
            show_colour(WHITE)
        elif current_time - time_start < 75.073:
            # cymbals
            show_colour(NOTHING)
        elif current_time - time_start < 83.237:
            # amazing rainbows
            bump_rainbow(5)
        elif current_time - time_start < 91.845:
            # amazing rainbows even faster
            bump_rainbow(2)
        elif current_time - time_start < 100.142:
            # hyper ultra
            bump_white_over_rainbow(2)
        elif current_time - time_start < 108.661:
            # synth solo
            bump_white_over_rainbow(1)
        else:
            show_colour(BLUE)
        pass
    sweeping_clear(0.1)
    print("blimey")

def shuffle_answer():
    numbers = ""
    for i in range(6):
        numbers += str(i)
    result = ""
    while numbers != "":
        char = random.choice(numbers)
        result += char
        numbers = numbers.replace(char, "")
        time.sleep(0.1)
    print("The answer is:", result)
    return result

reset()

correct_answer = "012345"
sequence_to_enter = correct_answer

last_keypress_heard = 0
last_button_pressed = -1

while True:
    if sequence_to_enter != correct_answer:
        # You got at least some of them right
        pix = ((len(correct_answer) - len(sequence_to_enter)) * num_pixels) // len(correct_answer)
        fill_rainbow_to(pix)
        hue_offset += 1

    event = keys.events.get()
    # event will be None if nothing has happened.
    if event:
        print(event)
        print(event.timestamp)
        if event.pressed:
            last_button_pressed = event.key_number
            if sequence_to_enter[0] == str(event.key_number):
                print("Correct!")
                sequence_to_enter = sequence_to_enter[1:]
            else:
                print("Wrong")
                sequence_to_enter = correct_answer
                reset()
            if sequence_to_enter == "":
                print("Unlocked the Secret Mode!")
                # Restart game:
                sequence_to_enter = correct_answer
                # Celebrate:
                play_song()
            last_keypress_heard = time.monotonic()
        if event.released:
            last_button_pressed = -1

    if last_button_pressed > 0 and time.monotonic() - last_keypress_heard > 10:
        # 0 starts the sequence, ignore that
        if last_button_pressed == 1:
            meadow()
            last_button_pressed = -1
        if last_button_pressed == 2:
            trans_pride()
            last_button_pressed = -1
        if last_button_pressed == 3:
            sunset()
            last_button_pressed = -1
        if last_button_pressed == 4:
            glitter()
            last_button_pressed = -1
        if last_button_pressed == 5:
            glow()
            last_button_pressed = -1
    time.sleep(0.01)
