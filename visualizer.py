import cv2
import numpy as np

class Visualizer:
    def __init__(self):
        self.generations = []
        self.best_fitness_values = []
        self.window_name = "Fitness Visualization"
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)

    def update_data(self, generation, best_fitness):
        """Update the data with the best fitness value of the current generation."""
        self.generations.append(generation)
        self.best_fitness_values.append(best_fitness)
        self.show_plot()

    def show_plot(self):
        """Display the real-time plot."""
        if not self.generations:
            return

        # Create a blank image
        img = np.zeros((600, 800, 3), dtype=np.uint8)
        
        # Define margins for the axes
        x_margin = 50
        y_margin = 50
        
        # Define the range for the y-axis
        y_min = -400
        y_max = 1000
        
        # Find the scaling factors for the plot
        x_scale = (800 - x_margin) / max(1, len(self.generations))
        y_scale = (600 - 2*y_margin) / (y_max - y_min)

        # Draw axes
        cv2.line(img, (x_margin, y_margin), (x_margin, 600 - y_margin), (255, 255, 255), 2)
        cv2.line(img, (x_margin, 600 - y_margin), (800 - x_margin, 600 - y_margin), (255, 255, 255), 2)

        # Plot each point in the fitness values list
        for i in range(1, len(self.best_fitness_values)):
            y1 = int(y_margin + (y_max - self.best_fitness_values[i-1]) * y_scale)
            y2 = int(y_margin + (y_max - self.best_fitness_values[i]) * y_scale)
            x1 = int(x_margin + (i-1) * x_scale)
            x2 = int(x_margin + i * x_scale)
            
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Add labels to the axes
        cv2.putText(img, 'Generation', (400, 590), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
        cv2.putText(img, 'Fitness', (10, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA, bottomLeftOrigin=True)

        # Add y-axis labels for the max and min values
        cv2.putText(img, str(y_max), (x_margin - 40, y_margin + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
        cv2.putText(img, str(y_min), (x_margin - 40, 600 - y_margin), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)

        # Show the plot in the named window
        cv2.imshow(self.window_name, img)
        cv2.waitKey(1)
