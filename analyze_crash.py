import numpy as np
import cv2

class CrashAnalyzer:
    def __init__(self):
        self.tolerance = 40
        self.color1 = [189, 255, 255]  # FFFBBD in RGB
        self.color2 = [0, 255, 255]    # FFFF00 in RGB

    def detect_color(self, region, colors):
        # Check if any pixel in the region is close to any of the specified colors within a tolerance
        for color in colors:
            lower_bound = np.array(color) - self.tolerance
            upper_bound = np.array(color) + self.tolerance
            mask = np.all(np.logical_and(region >= lower_bound, region <= upper_bound), axis=-1)
            if np.any(mask):
                return True
        return False

    def get_crash_detection(self, screenshot):
        # Define the coordinates for the region of interest (character bounding box)
        img_height, img_width, _ = screenshot.shape
        x1, x2 = 225, 300
        y1 = img_height // 2 - (253 - 181)
        y2 = img_height // 2 - (253 - 253)
        y1, y2 = min(y1, y2), max(y1, y2)

        # Get the region of interest from the screenshot (character box)
        character_box = screenshot[y1:y2, x1:x2]

        # Define the coordinates for the regions around the tires
        left_tire_region = character_box[41:44, 7:14]
        right_tire_region = character_box[39:43, 64:71]

        # Convert the colors from RGB to BGR (because OpenCV uses BGR format)
        left_tire_region = cv2.cvtColor(left_tire_region, cv2.COLOR_RGB2BGR)
        right_tire_region = cv2.cvtColor(right_tire_region, cv2.COLOR_RGB2BGR)

        # Check for crash indicators in the left and right tire regions
        left_crash = self.detect_color(left_tire_region, [self.color1, self.color2])
        right_crash = self.detect_color(right_tire_region, [self.color1, self.color2])

        # Determine if there was a crash based on the color detection in the tire regions
        return (left_crash and not right_crash) or (not left_crash and right_crash)
