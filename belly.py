import time
import random
import board
import keypad

from lights import Lights, RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE, PINK, WHITE, NOTHING
from music import Music

print("letsgooo")

keys = keypad.Keys((board.A0, board.A1, board.A2,board.A3,board.A4, board.A5), value_when_pressed=False, pull=True)
lights = Lights(board.NEOPIXEL, 60)
music = Music(board.D1, board.D10, board.D11)

def play_song():
    print("Playing song...")
    time_start = time.monotonic()
    while music.playing():
        current_time = time.monotonic()
        if current_time - time_start < 8.475:
            # first synth stab
            lights.bump_sunrise(0.1)
        elif current_time - time_start < 12.379:
            # second synth stab
            lights.bump_second_sunrise(0.05)
        elif current_time - time_start < 16.683:
            # third synth stab
            lights.bump_third_sunrise(0.05)
        elif current_time - time_start < 20.721:
            # rgss
            lights.bump_sparkles(0.2)
        elif current_time - time_start < 28.574:
            # rgss
            lights.bump_sparkles(0.1)
        elif current_time - time_start < 33.322:
            # RGSS
            lights.bump_sparkles(0.05)
        elif current_time - time_start < 50.005:
            # second singer
            lights.bump_fade_colours([ORANGE, PURPLE, BLUE], 3)
        elif current_time - time_start < 58.302:
            lights.bump_fade_colours([YELLOW, GREEN, CYAN, (0, 255, 50)], 2)
        elif current_time - time_start < 65.268:
            lights.bump_fade_colours([PINK, CYAN], 3)
        elif current_time - time_start < 66.821:
            # big solo
            lights.bump_fade_colours([PINK, CYAN, WHITE], 5)
        elif current_time - time_start < 72.766:
            # choir
            lights.show_colour(WHITE)
        elif current_time - time_start < 75.073:
            # cymbals
            lights.show_colour(NOTHING)
        elif current_time - time_start < 83.237:
            # amazing rainbows
            lights.bump_rainbow(5)
        elif current_time - time_start < 91.845:
            # amazing rainbows even faster
            lights.bump_rainbow(2)
        elif current_time - time_start < 100.142:
            # hyper ultra
            lights.bump_white_over_rainbow(2)
        elif current_time - time_start < 108.661:
            # synth solo
            lights.bump_white_over_rainbow(1)
        else:
            lights.show_colour(BLUE)
        pass
    lights.sweeping_clear(0.1)
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

lights.reset()

correct_answer = "012345"
sequence_to_enter = correct_answer

last_keypress_heard = 0
last_button_pressed = -1

while True:
    if sequence_to_enter != correct_answer:
        # You got at least some of them right
        pix = ((len(correct_answer) - len(sequence_to_enter)) * lights.num_pixels) // len(correct_answer)
        lights.fill_rainbow_to(pix)
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
                lights.reset()
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
            lights.meadow()
            last_button_pressed = -1
        if last_button_pressed == 2:
            lights.trans_pride()
            last_button_pressed = -1
        if last_button_pressed == 3:
            lights.sunset()
            last_button_pressed = -1
        if last_button_pressed == 4:
            lights.glitter()
            last_button_pressed = -1
        if last_button_pressed == 5:
            lights.glow()
            last_button_pressed = -1
    time.sleep(0.01)
