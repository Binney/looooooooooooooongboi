from audiomp3 import MP3Decoder
from audiobusio import I2SOut

class Music():
    def __init__(self, pin1, pin2, pin3):
        mp3_file = open("RGSS.mp3", "rb")
        self.decoder = MP3Decoder(mp3_file)
        self.audio = I2SOut(pin1, pin2, pin3)
    
    def play(self, filename):
        self.decoder.file = open(filename, "rb")
        self.audio.play(self.decoder)

    def playing(self):
        return self.audio.playing
