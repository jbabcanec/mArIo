import cv2
import pyautogui
import numpy as np
from pygetwindow import getWindowsWithTitle

class DirectionAnalyzer:
    def __init__(self):
        self.bsnes_window_title = '[HLE] Super Mario Kart (USA)'
        self.roi_x1, self.roi_y1, self.roi_x2, self.roi_y2 = 181, 96, 381, 190

    def count_pixels_in_range(self, image, lower_bound, upper_bound):
        mask = np.all(np.logical_and(image >= lower_bound, image <= upper_bound), axis=-1)
        return np.count_nonzero(mask)

    def detect_lakitu_direction(self, screenshot):
        try:
            game_window = getWindowsWithTitle(self.bsnes_window_title)[0]
        except IndexError:
            print(f"No window found with title: {self.bsnes_window_title}")
            return 'UNKNOWN'

        x, y, width, height = game_window._rect.left, game_window._rect.top, game_window._rect.width, game_window._rect.height
        height //= 2

        screenshot = pyautogui.screenshot(region=(x, y, width, height))
        screenshot_rgb = np.array(screenshot)

        lakitu_box = screenshot_rgb[self.roi_y1:self.roi_y2, self.roi_x1:self.roi_x2]

        required_colors = {
            "Orange": ([251, 100, 0], [255, 170, 60]),
            "Yellow": ([251, 190, 0], [255, 255, 100]),
            "Black": ([0, 0, 0], [40, 40, 40]),
            "White": ([200, 200, 200], [255, 255, 255]),
            "Red": ([180, 0, 0], [255, 50, 50])
        }

        min_pixel_count = 200

        for color_name, (lower_bound, upper_bound) in required_colors.items():
            pixel_count = self.count_pixels_in_range(lakitu_box, np.array(lower_bound), np.array(upper_bound))
            if pixel_count < min_pixel_count:
                return 'GOOD'

        return 'WRONG WAY'

    def get_direction(self):
        return self.detect_lakitu_direction(None)
