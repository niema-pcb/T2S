from gtts import gTTS
import pygame
import time
#import os

pygame.mixer.init()

while True:
    text = input("Say something (or type 'quit'): ")
    if text.lower() == "quit":
        break

    gTTS(text=text, lang="pl").save("output.mp3")

    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    pygame.mixer.music.unload()  # frees output.mp3 for the next round

pygame.mixer.quit()