import os
import pickle

class RoadMapping:
    
    def __init__(self, filepath="learning\\road_map.pkl"):
        self.filepath = filepath
        self.road_map = []
        
        # Create the learning directory if it doesn't exist
        if not os.path.exists('learning'):
            os.makedirs('learning')
        
        # Load existing road map if available
        self.load_road_map()
    
    def update_road_map(self, position, on_road):
        """Update the road map based on the current position and on-road detection."""
        if on_road == 'On Road':
            self.road_map.append(position)
    
    def get_road_map(self):
        """Get the current road map."""
        return self.road_map

    def save_road_map(self):
        """Save the road map to a file."""
        with open(self.filepath, 'wb') as file:
            pickle.dump(self.road_map, file)

    def load_road_map(self):
        """Load the road map from a file."""
        if os.path.exists(self.filepath):
            with open(self.filepath, 'rb') as file:
                self.road_map = pickle.load(file)
        else:
            print(f"No road map found at {self.filepath}, starting from scratch.")
