from src.chromosome import populate
from src.fitness import cost
from src.selection import selection
from src.crossover import crossover
from src.mutation import mutate_population
from pandas import DataFrame


def genetic_algorithm(
        employees: DataFrame,
        tasks: DataFrame, 
        population_size: int, 
        generations: int, 
        mutation_rate: int, 
        tournament_size: int, 
        elite_size: int
        )-> tuple[list[list[int]], list[float]]:

    """
    Runs the genetic algorithm to optimize task assignments among employees.

    Args:
        employees (pd.DataFrame): Employee data, including skills and available hours.
        tasks (pd.DataFrame): Task data, including required skills and hours.
        population_size (int): Number of chromosomes in the population.
        generations (int): Number of generations to run.
        mutation_rate (int): Mutation probability as a percentage [0, 100].
        tournament_size (int): Number of chromosomes participating in each tournament.
        elite_size (int): Number of best chromosomes preserved between generations.

    Returns:
        tuple[list[list[int]], list[float]]: The final population and the best cost from each generation.
    """

    population = populate(population_size, tasks.shape[0], employees.shape[0])

    generations_best_costs = []
    for generation in range(generations):

        costs = cost(population, employees, tasks)
        generations_best_costs.append(min(costs))
        indices = list(range(len(costs)))

        indices.sort(key=lambda i: costs[i], reverse=False)
        elite_indices = indices[:elite_size]
        new_population = [population[i] for i in elite_indices]

        new_population += crossover([population[i] for i in selection(costs, population_size - elite_size, tournament_size)])
        new_population = mutate_population(new_population, mutation_rate, employees.shape[0])

        population = new_population


    return population, generations_best_costs

