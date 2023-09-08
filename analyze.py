import numpy as np
import cv2
from analyze_place import PlaceAnalyzer
from analyze_crash import CrashAnalyzer
from analyze_speed import SpeedAnalyzer
from analyze_road import RoadAnalyzer

class ScreenAnalyzer:
    def __init__(self):
        self.place_analyzer = PlaceAnalyzer()
        self.crash_analyzer = CrashAnalyzer()
        self.speed_analyzer = SpeedAnalyzer()
        self.road_analyzer = RoadAnalyzer()

    def analyze(self, screenshot):
        screenshot_np = np.array(screenshot)

        # Capture the return value from each analyzer's method
        placement_output = self.place_analyzer.get_placement(screenshot_np)
        crash_detection_output = self.crash_analyzer.get_crash_detection(screenshot_np)
        speed_output = self.speed_analyzer.get_speed()
        on_road_detection_output = self.road_analyzer.get_on_road_detection(screenshot_np)

        # Create a black image to use as a canvas
        height, width, _ = screenshot_np.shape
        canvas = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Create a monitor using cv2 to visualize all the metrics
        font = cv2.FONT_HERSHEY_SIMPLEX
        color = (0, 255, 0)
        thickness = 2
        cv2.putText(canvas, f'Placement: {placement_output}', (10, 30), font, 0.7, color, thickness, cv2.LINE_AA)
        cv2.putText(canvas, f'Crash: {crash_detection_output}', (10, 60), font, 0.7, color, thickness, cv2.LINE_AA)
        cv2.putText(canvas, f'Accel: {round(speed_output, 2)} mph', (10, 90), font, 0.7, color, thickness, cv2.LINE_AA)
        cv2.putText(canvas, f'On Road: {on_road_detection_output}', (10, 120), font, 0.7, color, thickness, cv2.LINE_AA)

        # Display the metrics in a cv2 window
        cv2.imshow('Analysis Monitor', canvas)
        cv2.waitKey(1)
