import random
import numpy as np
import keyboard
import pickle
from visualizer import Visualizer


class GeneticAlgorithm:
    def __init__(self, population_size, mutation_rate):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.population = self.initialize_population()
        self.current_analysis_data = {}
        self.current_generation = 0
        self.visualizer = Visualizer()
    
    def initialize_population(self):
        """Initialize a population with random strategies."""
        population = []
        for _ in range(self.population_size):
            individual = self.create_random_individual()
            population.append(individual)
        return population

    def create_random_individual(self):
        """Create a random individual."""
        return np.random.randint(0, 2, 10)

    def save_data(self, filepath):
        data = {
            "population": self.population,
            "generation": self.current_generation,
        }
        with open(filepath, 'wb') as file:
            pickle.dump(data, file)

    def load_data(self, filepath):
        try:
            with open(filepath, 'rb') as file:
                data = pickle.load(file)
            self.population = data["population"]
            self.current_generation = data["generation"]
        except FileNotFoundError:
            print("No saved data found, starting from scratch.")


    def update_analysis_data(self, analysis_data):
        """
        Updates the genetic algorithm with the latest analysis data.

        Parameters:
        analysis_data (dict): A dictionary containing the latest analysis data.
        """
        self.current_analysis_data = analysis_data

    def fitness(self, individual):
        """Evaluate the fitness of an individual."""

        # Get the current analysis data
        data = self.current_analysis_data

        # Start with a base fitness score
        fitness_score = 0

        # Variables to track sustained good behavior
        sustained_speed_bonus = 0
        sustained_on_road_bonus = 0
        sustained_good_direction_bonus = 0

        # Evaluate 'placement': lower is better, 4 is neutral
        if data['placement']:
            placement = int(data['placement'])
            if placement < 4:
                fitness_score += (4 - placement) * 5

        # Evaluate 'crash_detection': False is good, True is bad
        if not data['crash_detection']:
            fitness_score += 20
        else:
            fitness_score -= 30

        # Evaluate 'speed': higher is better, with a quadratic bonus for higher speeds
        if data['speed'] > 0:
            speed_bonus = data['speed'] ** 2 / 100  # Quadratic scaling of the speed bonus
            fitness_score += speed_bonus

            # Check sustained high speed and reward accordingly
            if data['speed'] >= 80:  # You can adjust this threshold
                sustained_speed_bonus += 100
            else:
                sustained_speed_bonus = 0
            fitness_score += sustained_speed_bonus

            if data['speed'] == 100 and data['on_road_detection'] == 'On Road':
                speed_optimum_bonus = 200
                fitness_score += speed_optimum_bonus

        # Evaluate 'on_road_detection': 'On Road' is good
        if data['on_road_detection'] == 'On Road':
            fitness_score += 80

            # Check sustained on-road behavior and reward accordingly
            sustained_on_road_bonus += 100
        else:
            sustained_on_road_bonus = 0
        fitness_score += sustained_on_road_bonus

        # Evaluate 'direction': 'GOOD' is good, 'WRONG WAY' is bad
        if data['direction'] == 'GOOD':
            fitness_score += 30

            # Check sustained good direction and reward accordingly
            sustained_good_direction_bonus += 10
        else:  # Assuming the other value it can take is 'WRONG WAY'
            fitness_score -= 80
            sustained_good_direction_bonus = 0
        fitness_score += sustained_good_direction_bonus

        # Evaluate 'lap': incrementing is good, not incrementing for a long time is bad
        # Here we reward increase in lap number, but we will later introduce a mechanism
        # to penalize if no increment over a longer period
        if data['lap'] > 1:
            fitness_score += data['lap'] * 15

        return fitness_score

    def mutate(self, individual):
        """Mutate an individual with a certain probability."""
        for i in range(len(individual)):
            if random.random() < self.mutation_rate:
                # Flip the bit with a 50% chance
                if random.random() < 0.5:
                    individual[i] = 1 - individual[i]
                # Swap the current gene with another random gene in the individual with a 50% chance
                else:
                    swap_with = random.randint(0, len(individual) - 1)
                    individual[i], individual[swap_with] = individual[swap_with], individual[i]
        return individual

    def crossover(self, parent1, parent2):
        """Perform two-point crossover between two parents to produce offspring."""
        
        # Choose two random crossover points
        crossover_point1, crossover_point2 = sorted(random.sample(range(len(parent1)), 2))
        
        # Create offspring by combining genes of parents between the crossover points
        offspring1 = np.concatenate((parent1[:crossover_point1], parent2[crossover_point1:crossover_point2], parent1[crossover_point2:]))
        offspring2 = np.concatenate((parent2[:crossover_point1], parent1[crossover_point1:crossover_point2], parent2[crossover_point2:]))
        
        return offspring1, offspring2

    def select(self, k=6, elitism=0.1):
        """Select individuals using tournament selection with elitism."""
        
        selected_parents = []

        # Elitism: directly pass the top individuals to the next generation
        num_elites = int(elitism * self.population_size)
        fitness_values = [(ind, self.fitness(ind)) for ind in self.population]
        elites = [ind for ind, _ in sorted(fitness_values, key=lambda x: x[1], reverse=True)[:num_elites]]
        selected_parents.extend(elites)
        
        for _ in range(self.population_size - num_elites):
            # Tournament selection for the remaining individuals
            tournament_individuals = random.sample(self.population, k)
            fitness_values = [self.fitness(ind) for ind in tournament_individuals]
            selected_parents.append(tournament_individuals[np.argmax(fitness_values)])
        
        return selected_parents

    def create_new_generation(self):
        """Create a new generation using selection, crossover, and mutation."""
        # Select parents using tournament selection
        parents = self.select()

        # Create a new generation using crossover and mutation
        new_population = []
        for i in range(0, self.population_size, 2):
            parent1 = parents[i]
            parent2 = parents[i + 1]

            # Perform crossover to create offspring
            offspring1, offspring2 = self.crossover(parent1, parent2)

            # Perform mutation on the offspring
            offspring1 = self.mutate(offspring1)
            offspring2 = self.mutate(offspring2)

            #print('created new gen')

            # Add the offspring to the new population
            new_population.append(offspring1)
            new_population.append(offspring2)

        # Replace the old population with the new population
        self.population = new_population

    def run(self, generations):
        """Run the genetic algorithm for a number of generations."""
        for generation in range(self.current_generation, self.current_generation + generations):
            # Evaluate the fitness of each individual in the population
            fitness_values = [self.fitness(ind) for ind in self.population]

            # Create a new generation
            self.create_new_generation()
            
            # Optionally, print the best fitness value in this generation
            best_fitness = max(fitness_values)
            print(f"Generation {generation}: Best Fitness = {best_fitness}")

            # Update the plot data
            self.visualizer.update_data(generation, best_fitness)

            # Save the data at the end of each generation
            self.save_data(filepath="learning\\ga_data.pkl")
            print('saved data')
            self.current_generation += 1

        # Display the final plot
        self.visualizer.show_plot()

    def get_action(self):
        """Get the action to be performed by the AI."""
        # For now, return a random action from the population
        action = random.choice(self.population)
        print("Action chosen: ", action)
        return action
