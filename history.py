import os
import pickle

class HistoryHandler:
    
    def __init__(self, filepath="learning\\history_data.pkl"):
        self.filepath = filepath
        
        # Create the learning directory if it doesn't exist
        if not os.path.exists('learning'):
            os.makedirs('learning')
    
    def save(self, data):
        """Save the historical data to a file."""
        with open(self.filepath, 'ab') as file:
            pickle.dump(data, file)
    
    def load(self):
        """Load the historical data from a file."""
        if not os.path.exists(self.filepath):
            print(f"No historical data found at {self.filepath}, starting from scratch.")
            return []

        historical_data = []
        with open(self.filepath, 'rb') as file:
            while True:
                try:
                    historical_data.append(pickle.load(file))
                except EOFError:
                    break

        return historical_data
