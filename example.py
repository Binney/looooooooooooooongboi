import time
import random
import board
import keypad
import busio
import sdcardio
import storage

from lights import Lights, RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE, PINK, WHITE, NOTHING
from music import Music
import os

print("letsgooo")

keys = keypad.Keys((board.GP17, board.GP18, board.GP19, board.GP20, board.GP21), value_when_pressed=False, pull=True)
lights = Lights(board.GP0, 60)
music = Music(board.GP1, board.GP2, board.GP3)

spi = busio.SPI(board.GP14, board.GP15, board.GP12)
cs = board.GP13

song_list = ["dale.mp3"]
sfx_list = ["dale.mp3"]

def shuffle(list):
    # no shuffle in circuitpython random
    while len(list) > 0:
        index = random.randint(0, len(list) - 1)
        yield list.pop(index)

songs_that_are_cursed = [
    "mii.mp3",
    "Flying_Kerfuffle.mp3"
]

try:
    sdcard = sdcardio.SDCard(spi, cs)
    vfs = storage.VfsFat(sdcard)
    storage.mount(vfs, "/sd")

    music_files = os.listdir("/sd/music")
    song_list = [f for f in music_files if not f.startswith("._") and not f in songs_that_are_cursed and (f.endswith('.mp3') or f.endswith('.wav'))]
    song_list = list(shuffle(song_list))

    sound_files = os.listdir("/sd/sounds")
    sfx_list = [f for f in sound_files if not f.startswith("._") and (f.endswith('.mp3') or f.endswith('.wav'))]
    sfx_list = list(shuffle(sfx_list))

except Exception as e:
    print("SD Card Mount Error:", e)

current_song = -1
current_sfx = -1

def play_next_song():
    global current_song
    current_song = (current_song + 1) % len(song_list)
    song_to_play = song_list[current_song]
    print(f"Playing song: {song_to_play}")
    music.stop()
    music.play(f"/sd/music/{song_to_play}")

def play_next_sfx():
    global current_sfx
    current_sfx = (current_sfx + 1) % len(sfx_list)
    sfx_to_play = sfx_list[current_sfx]
    print(f"Playing song: {sfx_to_play}")
    music.stop()
    music.play(f"/sd/sounds/{sfx_to_play}")

lights.reset()

last_keypress_heard_time = 0
last_button_pressed = -1

current_lights = 0

while True:
    event = keys.events.get()
    # event will be None if nothing has happened.
    if event:
        print(event)
        print(event.timestamp)
        if event.pressed:
            last_button_pressed = event.key_number
            last_keypress_heard_time = time.monotonic()
        if event.released:
            last_button_pressed = -1

    if current_lights == 0:
        lights.bump_rainbow(1)
    elif current_lights == 1:
        lights.bump_sunset()
    elif current_lights == 2:
        lights.bump_trans_pride()
    elif current_lights == 3:
        lights.bump_glitter()
    elif current_lights == 4:
        lights.bump_glow()
    elif current_lights == 5:
        lights.bump_meadow()
    else:
        lights.reset()

    if last_button_pressed >= 0 and time.monotonic() - last_keypress_heard_time > 1:
        print("time to do a thing!", last_button_pressed)
        if last_button_pressed == 0:
            play_next_song()
            last_button_pressed = -1
        if last_button_pressed == 1:
            play_next_sfx()
            last_button_pressed = -1
        if last_button_pressed == 2:
            current_lights = (current_lights + 1) % 6
            last_button_pressed = -1
        if last_button_pressed == 3:
            # just switch off lights
            current_lights = -1
            last_button_pressed = -1
    time.sleep(0.01)
