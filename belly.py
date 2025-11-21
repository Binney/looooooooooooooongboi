import time
import random
import board
import keypad

from audioio import AudioOut
from audiomp3 import MP3Decoder
from audiobusio import I2SOut

print("letsgooo")

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
