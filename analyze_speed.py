class SpeedAnalyzer:
    def __init__(self):
        self.speed = 0  # Variable to keep track of the current speed
        self.MAX_SPEED = 100  # Maximum possible speed
        self.ACCELERATION_RATE = 10  # Increased rate of acceleration
        self.DECELERATION_RATE = 20  # Decreased rate of deceleration

    def update_speed_based_on_action(self, action):
        # Here, we check the sixth element in the action list to determine whether to accelerate
        if action[5] == 1:  
            self.speed = min(self.MAX_SPEED, self.speed + self.ACCELERATION_RATE)
        else:
            self.speed = max(0, self.speed - self.DECELERATION_RATE)

    def get_speed(self):
        # Simply return the current speed without checking button presses
        return self.speed
