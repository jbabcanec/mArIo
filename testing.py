import pygame
import keyboard
import time

class SpeedAnalyzer:
    def __init__(self):
        pygame.init()  # Ensure pygame is initialized
        self.joystick_count = pygame.joystick.get_count()
        if self.joystick_count > 0:
            self.my_joystick = pygame.joystick.Joystick(0)
            self.my_joystick.init()

        self.speed = 0  # Variable to keep track of the current speed
        self.MAX_SPEED = 100  # Maximum possible speed
        self.ACCELERATION_RATE = 10  # Rate of acceleration
        self.DECELERATION_RATE = 20  # Rate of deceleration

    def check_button_presses(self):
        pygame.event.pump()  # Update the event queue

        b_button_pressed = self.my_joystick.get_button(1) if self.joystick_count > 0 else False
        i_key_pressed = keyboard.is_pressed('I')  # Check for 'I' key press using the keyboard library

        if b_button_pressed or i_key_pressed:
            self.speed = min(self.MAX_SPEED, self.speed + self.ACCELERATION_RATE)
        else:
            self.speed = max(0, self.speed - self.DECELERATION_RATE)

    def get_speed(self):
        self.check_button_presses()  # Check the button presses each time get_speed is called
        return self.speed  # Return the current speed


# Main block to test the SpeedAnalyzer class
if __name__ == "__main__":
    speed_analyzer = SpeedAnalyzer()  # Create an instance of the SpeedAnalyzer class

    while True:
        speed = speed_analyzer.get_speed()  # Get the current speed
        print(f"Current speed: {speed}")  # Print the current speed
        time.sleep(0.1)  # Sleep for a short time to reduce the number of print statements
