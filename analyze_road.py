import cv2
import numpy as np

class RoadAnalyzer:
    def __init__(self):
        # Define a threshold value for the average pixel intensity 
        # to determine if there is dust (this value might need tuning)
        self.dust_threshold = 50

    def get_on_road_detection(self, screenshot_np):
        # Get the dimensions of the screenshot
        img_height, img_width, _ = screenshot_np.shape

        # Define the coordinates for the region of interest (character bounding box)
        x1, x2 = 225, 300
        y1 = img_height // 2 - (253 - 181)
        y2 = img_height // 2 - (253 - 253)
        
        # Define smaller regions of interest at the bottom corners of the character bounding box
        bottom_left_region = screenshot_np[y2-20:y2, x1:x1+20]
        bottom_right_region = screenshot_np[y2-20:y2, x2-20:x2]
        
        # Convert these regions to grayscale
        bottom_left_gray = cv2.cvtColor(bottom_left_region, cv2.COLOR_BGR2GRAY)
        bottom_right_gray = cv2.cvtColor(bottom_right_region, cv2.COLOR_BGR2GRAY)
        
        # Apply thresholding to isolate the dust pixels
        _, bottom_left_thresh = cv2.threshold(bottom_left_gray, 127, 255, cv2.THRESH_BINARY)
        _, bottom_right_thresh = cv2.threshold(bottom_right_gray, 127, 255, cv2.THRESH_BINARY)
        
        # Calculate the average pixel intensity in these regions
        bottom_left_avg_intensity = np.mean(bottom_left_thresh)
        bottom_right_avg_intensity = np.mean(bottom_right_thresh)
        
        # Determine if the character is on or off the road based on the average pixel intensity
        if bottom_left_avg_intensity > self.dust_threshold or bottom_right_avg_intensity > self.dust_threshold:
            return 'Off Road'
        else:
            return 'On Road'