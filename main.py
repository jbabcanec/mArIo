import pygame
import keyboard
import time
import numpy as np

from analyze import ScreenAnalyzer
from recording_handler import RecordingHandler

pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

bsnes_window_title = '[HLE] Super Mario Kart (USA)'

# Create a single ScreenAnalyzer instance to be used for all analyses
analyzer = ScreenAnalyzer()

def analyze_screen(screenshot):
    # Use the existing analyzer instance to analyze the screenshot
    analyzer.analyze(np.array(screenshot))

recording_handler = RecordingHandler(bsnes_window_title, analyze_screen)

# Set up hotkey to toggle recording
keyboard.on_press_key('space', lambda _: recording_handler.toggle_recording())

# Keeping the script running
while True:
    pygame.event.get()  # Update the event queue continuously
    time.sleep(0.1)
