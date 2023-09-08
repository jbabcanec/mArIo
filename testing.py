import cv2
import pyautogui
import os
from pygetwindow import getWindowsWithTitle

# Define the window title of the game (adjust as needed)
bsnes_window_title = '[HLE] Super Mario Kart (USA)'

# Specify the directory where you want to save the screenshots
output_directory = "C:\\Users\\josep\\Dropbox\\Babcanec Works\\Programming\\mArIo\\reinforcement\\screenshots"

# Create output directory if it does not exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

def capture_screenshot():
    # Get the game window
    try:
        game_window = getWindowsWithTitle(bsnes_window_title)[0]
    except IndexError:
        print(f"No window found with title: {bsnes_window_title}")
        return

    # Get the coordinates of the game window
    x, y, width, height = game_window._rect.left, game_window._rect.top, game_window._rect.width, game_window._rect.height
    
    # Modify the height to capture only the upper half of the window
    height //= 2

    # Capture a screenshot of the upper half of the game window using pyautogui
    screenshot = pyautogui.screenshot(region=(x, y, width, height))

    # Save the screenshot to the output directory
    screenshot.save(os.path.join(output_directory, 'lakitu_sample.png'))

# Call the function to capture the screenshot
capture_screenshot()
