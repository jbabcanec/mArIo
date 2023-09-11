import pygame
import keyboard
import time
import numpy as np
from ai_controller import ai_control
from analyze import ScreenAnalyzer
from recording_handler import RecordingHandler

pygame.init()
pygame.joystick.init()

bsnes_window_title = '[HLE] Super Mario Kart (USA)'

# Create a single ScreenAnalyzer instance to be used for all analyses
analyzer = ScreenAnalyzer()

def analyze_screen(screenshot):
    # Use the existing analyzer instance to analyze the screenshot
    analyzer.analyze(np.array(screenshot))

recording_handler = RecordingHandler(bsnes_window_title, analyze_screen)

# Set up hotkey to toggle recording
keyboard.on_press_key('space', lambda _: recording_handler.toggle_recording())

# Simulation loop for AI control
while True:
    pygame.event.get()  # Update the event queue continuously
    
    # Here, we create an action dictionary to represent continuously pressing the "I" key
    action = {"w": False, "a": False, "s": False, "d": False, "u": False, "i": True, "o": False, "p": False, "9": False, "0": False}
    
    # Send the action dictionary to the ai_control function to control the game
    ai_control(action)
    
    time.sleep(0.1)
