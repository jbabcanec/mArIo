import cv2
import time
import pytesseract
import numpy as np
import re

class LapAnalyzer:
    def __init__(self):
        self.lap_sign_config = '--psm 6'
        self.lap_start_time = None
        self.lap_count = 1
        self.lap_update_time = 0

    def get_lap(self, screenshot_np):
        roi_x1, roi_y1, roi_x2, roi_y2 = 185, 135, 253, 177
        
        roi = screenshot_np[roi_y1:roi_y2, roi_x1:roi_x2]
        
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        _, thresholded_roi = cv2.threshold(gray_roi, 100, 255, cv2.THRESH_BINARY)
        
        cv2.imshow('ROI', roi)
        cv2.imshow('Processed ROI', thresholded_roi)

        lap_sign = pytesseract.image_to_string(thresholded_roi, config=self.lap_sign_config).strip()

        if re.search(r"(l.a?|la.)\s?|a?[pl]\s?\d?", lap_sign, re.IGNORECASE):
            if self.lap_start_time is None:
                self.lap_start_time = time.time()
            elapsed_time = time.time() - self.lap_start_time
            if elapsed_time >= 0.15 and time.time() - self.lap_update_time >= 20:
                self.lap_count += 1
                self.lap_start_time = None
                self.lap_update_time = time.time()
        else:
            self.lap_start_time = None
        
        return self.lap_count
