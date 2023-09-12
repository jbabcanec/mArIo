import random
import numpy as np
import keyboard
import pickle


class GeneticAlgorithm:
    def __init__(self, population_size, mutation_rate):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.population = self.initialize_population()
        self.current_analysis_data = {}
        self.current_generation = 0
    
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

        # Evaluate 'placement': lower is better, 4 is neutral
        if data['placement']:
            placement = int(data['placement'])
            if placement < 4:
                fitness_score += (4 - placement) * 5
            # No penalty or reward for placement 4 as it is neutral

        # Evaluate 'crash_detection': False is good, True is bad
        if not data['crash_detection']:
            fitness_score += 20
        else:
            fitness_score -= 30

        # Evaluate 'speed': higher is better, especially if on road and direction is good
        if data['speed'] > 0:
            speed_bonus = data['speed']
            if data['on_road_detection'] == 'On Road' and data['direction'] == 'GOOD':
                speed_bonus *= 2  # Double the bonus if on road and going in the right direction
            fitness_score += speed_bonus

        # Evaluate 'on_road_detection': 'On Road' is good
        if data['on_road_detection'] == 'On Road':
            fitness_score += 50

        # Evaluate 'direction': 'GOOD' is good, 'WRONG WAY' is bad
        if data['direction'] == 'GOOD':
            fitness_score += 30
        else:  # Assuming the other value it can take is 'WRONG WAY'
            fitness_score -= 80

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
                # Change the gene to a random binary value (0 or 1)
                individual[i] = 1 - individual[i]  # This flips the bit, 0 becomes 1 and 1 becomes 0
        return individual

    def crossover(self, parent1, parent2):
        """Perform crossover between two parents to produce offspring."""
        # Choose a random crossover point
        crossover_point = random.randint(0, len(parent1) - 1)
        
        # Create two offspring by combining the genes of the parents
        offspring1 = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))
        offspring2 = np.concatenate((parent2[:crossover_point], parent1[crossover_point:]))
        
        return offspring1, offspring2

    def select(self, k=3):
        """Select individuals to act as parents for the next generation using tournament selection.

        Parameters:
        k (int): The number of individuals to select for each tournament.
        """
        selected_parents = []

        for _ in range(self.population_size):
            # Select k individuals randomly from the population for the tournament
            tournament_individuals = random.sample(self.population, k)
            
            # Evaluate the fitness of the selected individuals
            fitness_values = [self.fitness(ind) for ind in tournament_individuals]
            
            # Select the individual with the highest fitness
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

            # Save the data at the end of each generation
            self.save_data(filepath="C:\\Users\\josep\\Dropbox\\Babcanec Works\\Programming\\mArIo\\reinforcement\\learning\\ga_data.pkl")
            print('saved data')
            self.current_generation += 1

    def get_action(self):
        """Get the action to be performed by the AI."""
        # For now, return a random action from the population
        action = random.choice(self.population)
        print("Action chosen: ", action)
        return action
