import keyboard

KEY_MAPPING = ['w', 'a', 's', 'd', 'u', 'i', 'o', 'p', '9', '0']

def perform_action(action):
    """Perform the action represented by the action encoding."""
    for index, key_state in enumerate(action):
        key_name = KEY_MAPPING[index]
        if key_state:
            keyboard.press(key_name)
        else:
            keyboard.release(key_name)

