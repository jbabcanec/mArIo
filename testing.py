import pickle
from pprint import pprint

def read_pickle_file(filepath):
    """Read and print the contents of a pickle file."""
    try:
        with open(filepath, 'rb') as file:
            while True:
                try:
                    data = pickle.load(file)
                    pprint(data)
                except EOFError:
                    break
    except FileNotFoundError:
        print(f"No data found at {filepath}.")

# Filepaths to your pickle files
road_map_filepath = "learning\\road_map.pkl"
history_data_filepath = "learning\\history_data.pkl"

# Read and print the contents of the road map pickle file
print("Contents of the road map pickle file:")
read_pickle_file(road_map_filepath)

# Read and print the contents of the history data pickle file
print("\nContents of the history data pickle file:")
read_pickle_file(history_data_filepath)
