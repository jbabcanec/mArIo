import pyautogui

# Move the current_states dictionary outside of the ai_control function
current_states = {"w": False, "a": False, "s": False, "d": False, "u": False, "i": False, "o": False, "p": False, "9": False, "0": False}

def ai_control(action):
    """
    Use pyautogui to send control signals based on the AI's action.

    Parameters:
    action (dict): A dictionary representing the AI's current action. 
    """
    # Define the controls mapping
    controls = {
        "w": "up",
        "a": "left",
        "s": "down",
        "d": "right",
        "u": "A",
        "i": "B",
        "o": "X",
        "p": "Y",
        "9": "L",
        "0": "R"
    }
    
    # Loop over each control and activate the corresponding keyboard control
    for key, status in action.items():
        if status != current_states[key]:
            if status:
                pyautogui.keyDown(controls.get(key, key))
            else:
                pyautogui.keyUp(controls.get(key, key))
                
            # Update the current state of the key
            current_states[key] = status
