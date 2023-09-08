import pyautogui
import time
import threading
from pygetwindow import getWindowsWithTitle

class RecordingHandler:
    def __init__(self, window_title, analyze_callback):
        self.window_title = window_title
        self.bsnes_window = self.get_window()
        self.is_recording = False
        self.analyze_callback = analyze_callback

    def get_window(self):
        try:
            return getWindowsWithTitle(self.window_title)[0]
        except IndexError:
            print(f"No window found with title: {self.window_title}")
            return None

    def capture_screen(self):
        if self.bsnes_window is None:
            print("BSNES window is not open")
            return None

        rect = self.bsnes_window._rect
        x, y, width, height = rect.left, rect.top, rect.width, rect.height
        screenshot = pyautogui.screenshot(region=(x, y, width, height))
        return screenshot

    def record(self):
        self.is_recording = True
        while self.is_recording:
            screenshot = self.capture_screen()
            if screenshot is not None:
                self.analyze_callback(screenshot)
            time.sleep(0.1)

    def stop_record(self):
        self.is_recording = False

    def toggle_recording(self):
        self.is_recording = not self.is_recording
        if self.is_recording:
            print("Recording ON")
            threading.Thread(target=self.record).start()
        else:
            print("Recording OFF")
            self.stop_record()
