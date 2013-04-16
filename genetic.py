"""
    Requirements:
        * A genetic representation of the rocket
        * Fitness function to evaluate fitness of the rocket
        End point: A certain height or number of generations
        Mutation probability
        Population size

    Steps:
        Initialize a population

        while end point hasn't been reached:
            Determine fittest rockets (proportion of total pop)
            Combine randomly
            Mutate
            Evaluate for end point

"""

import rocket_utils
from rocket_utils import random_engine, random_fuel
from random import randint
from matplotlib import pyplot
from datetime import datetime


class Rocket(object):
    """
        Genetic representation of a rocket
        3 Stages
        genes: two integers for each stage
                    0: Fuel tank size
                    1: Rocket type
    """
    def __init__(self, new_genes):
        super(Rocket, self).__init__()
        if not new_genes:
            self.genes = [0, 0, 0, 0, 0, 0]
        else:
            self.genes = new_genes

        self.fitness = None
        # Evaluate fitness on creation
        self.evaulate_fitness()

    # Function that determines the fitness of the Rocket
    def evaulate_fitness(self):
        self.fitness = sum(self.genes)

    # Randomly mutate one 'gene' sequence
    def mutate(self):
        rand_int = randint(0, len(self.genes) - 1)
        # If odd, is engine type
        if rand_int % 2 != 0:
            self.genes[rand_int] = random_engine()
        # if even, fuel tank size
        else:
            self.genes[rand_int] = random_fuel()

    # Print
    def display(self):
        print(self.genes)
        print("Fitness: {}".format(self.fitness))


################################
# GeneticOptmizer
################################
class GeneticOptimizer(object):
    """Base class for genetic algorithms"""
    def __init__(self):

        self.initialize_run()

    # Runs through the whole optmization algorithm
    def run_optimizer(self):
        self.display_starting_summary()
        self.initialize_run()
        self.initialize_population()

        while not self.end_point_reached():
            fittest_population = self.get_fittest()

            self.combine_fittest(fittest_population)
            self.mutate()
            self.sort_population()
            self.current_generation += 1

            self.log_results()

    # Sets the configuration to its starting state
    def initialize_run(self):
        self.population = []
        self.current_generation = 0
        self.fitness_history = []
        self.start_time = datetime.now()
        self.current_time = None

    def evaluate_population(self):
        for item in self.population:
            item.evaulate_fitness()

    # Sorts the population by fitness. Lower index have lower fitness
    def sort_population(self):
        self.population = sorted(self.population, key=lambda item: item.fitness)

    def display_population(self):
        print("\nGeneration {}:".format(self.current_generation))
        for item in self.population:
            item.display()

        print("\nAverage fitness: {}".format(self.average_fitness()))

    # Returns the average fitness of current population
    def average_fitness(self):
        average = 0

        for item in self.population:
            average += item.fitness
        return average / len(self.population)

    # Return the max and min fitness present in current population
    def max_fitness(self):
        return self.population[-1].fitness

    def min_fitness(self):
        return self.population[0].fitness

    # The functions below are abstract and left up to whatever class is
    # based off this one
    def initialize_population(self):
        pass

    def display_starting_summary(self):
        pass

    def end_point_reached(self):
        pass

    def get_fittest(self):
        pass

    def combine_fittest(self, fittest_population):
        pass

    def mutate(self):
        pass

    def log_results(self):
        pass

    def save_log(self):
        pass


################################
# RocketOptimizer
################################
class RocketOptimizer(GeneticOptimizer):
    """Implements genetic algorithm to create an optimal rocket"""
    def __init__(self, config=[]):
        super(RocketOptimizer, self).__init__()

        if config != []:
            self.init_from_config(config)

        self.population_size = 50
        self.max_generations = 400
        # Number that will go on to breed
        self.num_fittest = 50
        # The percent mutation is based off this ratio. 100 means 1/100=1%,
        # 1000 means 1/1000=.1% etc
        self.mutation_ratio = 100
        # threshold/mutation_ratio = percent of population that will mutate
        self.mutation_threshold = 5

    def init_from_config(self, config):
        self.population_size = config['population_size']
        self.max_generations = config['max_generations']
        self.num_fittest = config['num_fittest']
        self.mutation_ratio = config['mutation_ratio']
        self.mutation_threshold = config['mutation_threshold']

    def display_starting_summary(self):
        print("\nPopulation size: {} | Breeding pop size: {} | Max # generations: {}".format(
               self.population_size, self.num_fittest, self.max_generations))

        print("Mutation chance: {}/{}".format(self.mutation_threshold, self.mutation_ratio))

    def initialize_population(self):
        # Create random Rockets

        for x in range(0, self.population_size):
            self.population.append(self.create_random_rocket())

        self.sort_population()

    def create_random_rocket(self):
        return Rocket([
            random_fuel(), random_engine(),
            random_fuel(), random_engine(),
            random_fuel(), random_engine(),
        ])

    def end_point_reached(self):
        return self.current_generation > self.max_generations

    def get_fittest(self):
        return self.population[self.population_size - self.num_fittest:]

    def combine_fittest(self, fittest_population):
        new_population = []

        for x in range(0, self.population_size):
            new_population.append(self.breed_two(fittest_population))

        self.population = new_population

    # Breeds two random Rockets and returns the new Rocket
    def breed_two(self, breeding_pop):
        # The fitter rockets should have a better chance to breed
        # Find two random items from the breeding population
        first_index = randint(0, self.num_fittest - 1)
        second_index = randint(0, self.num_fittest - 1)

        # Extract the genes
        first = breeding_pop[first_index].genes
        second = breeding_pop[second_index].genes

        # Get random index to split on, with at least 2 genes
        rand_split = randint(1, len(first) - 1)
        new_genes = first[:rand_split] + second[rand_split:]

        return Rocket(new_genes)

    def mutate(self):
        for rocket in self.population:
            rand_int = randint(0, self.mutation_ratio - 1)

            if rand_int < self.mutation_threshold:
                rocket.mutate()

    # Adds current generation's summary to the history
    def log_results(self):
        self.fitness_history.append([
            self.average_fitness(),
            self.max_fitness(),
            self.min_fitness()
        ])

        # Every so many generations display the progress
        if self.current_generation % 200 == 0:
            self.display_progress()

    # Displays current generation # and estimated time remaining
    def display_progress(self):
        self.current_time = datetime.now()
        time_diff = self.current_time - self.start_time
        elapsed_time = time_diff.seconds
        percent_done = self.max_generations / float(self.current_generation)

        time_remaining = ((1 - percent_done) * elapsed_time) / 60.0
        time_remaining = round(-1 * time_remaining, 2)

        print("{} - Time remaining: {} minutes".format(self.current_generation, time_remaining))

    # Save the fitness_history to a file
    def save_log(self):
        rocket_utils.save_csv(self.fitness_history, self.create_log_name() + '.csv')
        self.save_graph()

    # Returns semi-unique identifier for file naming purposes
    def create_log_name(self):
        return "pop-{}_fit-{}_gen-{}_mut-{}-{}".format(
            self.population_size, self.num_fittest,
            self.max_generations, self.mutation_ratio,
            self.mutation_threshold)

    # Show plot
    def plot(self):
        pyplot.plot(self.fitness_history)
        pyplot.show()

    # Save graph to file
    def save_graph(self):
        pyplot.plot(self.fitness_history)

        figure = pyplot.gcf()
        figure.set_size_inches(30, 15)

        pyplot.savefig("{}.png".format(self.create_log_name()))

    # Clears plots, resets optimzer runs etc
    def reset(self):
        self.initialize_run()
        pyplot.clf()


################################
# Main
################################
if __name__ == "__main__":
    optimizer = RocketOptimizer()

    config = {
        'population_size': 50,
        'max_generations': 400,
        'num_fittest': 50,
        'mutation_ratio': 1000,
        'mutation_threshold': 1,
    }

    # # 2-10
    # for x in range(2, 10, 2):
    #     config['num_fittest'] = x
    #     optimizer.init_from_config(config)
    #     optimizer.run_optimizer()
    #     optimizer.plot()
    #     optimizer.save_log()
    #     optimizer.reset()

    # 25-500
    for x in range(1, 21):
        config['num_fittest'] = int(((x * 5) / 100.0) * optimizer.population_size)
        optimizer.init_from_config(config)
        optimizer.run_optimizer()
        optimizer.plot()
        optimizer.save_log()
        optimizer.reset()

    # # 490-498
    # for x in range(245, 250):
    #     config['num_fittest'] = x * 2
    #     optimizer.init_from_config(config)
    #     optimizer.run_optimizer()
    #     optimizer.plot()
    #     optimizer.save_log()
    #     optimizer.reset()
