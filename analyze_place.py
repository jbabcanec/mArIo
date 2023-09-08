import cv2
from pytesseract import pytesseract
from statistics import mode, StatisticsError

class PlaceAnalyzer:
    def __init__(self):
        self.sample_saved = False
        self.previous_placements = [None] * 5
        self.last_valid_placement = self.read_last_valid_placement_from_file()
        self.template_1 = cv2.imread('C:\\Users\\josep\\Dropbox\\Babcanec Works\\Programming\\mArIo\\reinforcement\\image_recognition_templates\\template_1.png', 0)

    def get_placement(self, screenshot):
        try:
            max_val = 0.0
            height, _, _ = screenshot.shape
            top_half_screenshot = screenshot[:height//2, :]
            y1, y2 = 205 - (height // 2), 254 - (height // 2)
            x1, x2 = 454, 492
            region = top_half_screenshot[y1:y2, x1:x2]
            region_gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
            region_thresh = cv2.adaptiveThreshold(region_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 3))
            region_morph = cv2.morphologyEx(region_thresh, cv2.MORPH_CLOSE, kernel)
            placement_text = pytesseract.image_to_string(region_morph, config='--psm 8')
            placement = ''.join(filter(str.isdigit, placement_text))

            if not placement or placement == '4':
                template_resized = cv2.resize(self.template_1, (region_morph.shape[1], region_morph.shape[0]))
                res = cv2.matchTemplate(region_morph, template_resized, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(res)
                if abs(max_val) > 0.45 or (placement == '4' and self.previous_placements[-1] == 2):
                    placement = '1'

            if placement and 1 <= int(placement) <= 8:
                self.previous_placements.pop(0)
                self.previous_placements.append(int(placement))

                # Check if the new placement is significantly different from the recent valid placements
                recent_placements = [p for p in self.previous_placements if p is not None]
                if recent_placements and abs(int(placement) - int(self.last_valid_placement)) > 2:
                    # If the new placement is significantly different, use the mode of the recent valid placements
                    # as the new placement (if there is a mode)
                    try:
                        placement = mode(recent_placements)
                    except StatisticsError:
                        # If there is no mode, keep the new placement
                        pass

                self.last_valid_placement = placement
                self.write_last_valid_placement_to_file(placement)
            else:
                pass
        except Exception as e:
            #print(f"Could not get placement: {e}")
            pass

        return self.last_valid_placement

    def read_last_valid_placement_from_file(self):
        try:
            with open('C:\\Users\\josep\\Dropbox\\Babcanec Works\\Programming\\mArIo\\reinforcement\\utils\\last_valid_placement.txt', 'r') as file:
                last_valid_placement = file.read().strip()
                if last_valid_placement.isdigit() and 1 <= int(last_valid_placement) <= 8:
                    return last_valid_placement
                else:
                    return '4'
        except FileNotFoundError:
            return '4'

    def write_last_valid_placement_to_file(self, placement):
        with open('C:\\Users\\josep\\Dropbox\\Babcanec Works\\Programming\\mArIo\\reinforcement\\utils\\last_valid_placement.txt', 'w') as file:
            file.write(placement)
