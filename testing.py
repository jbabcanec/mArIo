import keyboard
import time

time.sleep(5)  # Gives you 5 seconds to switch to the game window

while True:
    keyboard.press('i')
    time.sleep(0.1)
    keyboard.release('i')
