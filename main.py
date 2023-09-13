import pygame
import keyboard
import time
import numpy as np
from analyze import ScreenAnalyzer
from recording_handler import RecordingHandler
from genetic_algorithm import GeneticAlgorithm
from encoding import perform_action

pygame.init()
pygame.joystick.init()

bsnes_window_title = '[HLE] Super Mario Kart (USA)'

# Create a single ScreenAnalyzer instance to be used for all analyses
analyzer = ScreenAnalyzer()

# Initialize the genetic algorithm
genetic_algorithm_instance = GeneticAlgorithm(population_size=20, mutation_rate=0.1)

# Load any previously saved data
genetic_algorithm_instance.load_data(filepath="learning\\ga_data.pkl")

# Run the genetic algorithm for a small number of generations to initiate the population
#genetic_algorithm_instance.run(generations=10)

def analyze_screen(screenshot):
    # Convert the screenshot to a numpy array for analysis
    screenshot_np = np.array(screenshot)

    # Use the existing analyzer instance to analyze the screenshot
    analyzer.analyze(screenshot_np)
    
    # Get the analysis data
    analysis_data = {
        "placement": analyzer.place_analyzer.get_placement(screenshot_np),
        "crash_detection": analyzer.crash_analyzer.get_crash_detection(screenshot_np),
        "speed": analyzer.speed_analyzer.get_speed(),
        "on_road_detection": analyzer.road_analyzer.get_on_road_detection(screenshot_np),
        "direction": analyzer.direction_analyzer.get_direction(),
        "lap": analyzer.lap_analyzer.get_lap(screenshot_np),
    }
    
    # Update the genetic algorithm with the analysis data
    genetic_algorithm_instance.update_analysis_data(analysis_data)

recording_handler = RecordingHandler(bsnes_window_title, analyze_screen)

# Variable to keep track of whether the AI is controlling the game
ai_control_enabled = False

def toggle_ai_control():
    global ai_control_enabled
    ai_control_enabled = not ai_control_enabled
    recording_handler.toggle_recording()

# Set up a hotkey to toggle recording and AI control
keyboard.on_press_key('space', lambda _: toggle_ai_control())

generation_interval = 200  # Adjust this value as needed
generation_counter = 0

while True:
    pygame.event.get()  # Update the event queue continuously
    
    if ai_control_enabled:
        # Get the action from the genetic algorithm
        action = genetic_algorithm_instance.get_action()
        
        # Perform the action using the action encoding
        perform_action(action)

        # Update the speed based on the AI's action
        # We do this because all other data is read from screenshot
        # whereas the speed is read from button presses
        analyzer.speed_analyzer.update_speed_based_on_action(action)
        
        # Increment the generation counter
        generation_counter += 1
        
        # Run the genetic algorithm for a few generations at regular intervals
        if generation_counter % generation_interval == 0:
            genetic_algorithm_instance.run(generations=1)
            generation_counter = 0
    
    time.sleep(0.05)

