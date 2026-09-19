from .chromosome import populate
from .crossover import crossover
from .fitness import cost
from .mutation import mutate_population
from .preprocessing import EmployeeData, TaskData
from .selection import selection


def genetic_algorithm(
    employees_data: list[EmployeeData],
    tasks_data: list[TaskData],
    population_size: int,
    generations: int,
    mutation_rate: int,
    tournament_size: int,
    crossover_type: str,
    elite_size: int,
) -> tuple[list[list[int]], list[list[float | list[float] | list[int]]]]:
    """
    Run the genetic algorithm to optimize task assignments among employees.

    The algorithm creates an initial population of task assignments and
    evolves it over multiple generations using tournament selection,
    crossover, mutation, and elitism.

    Args:
        employees_data (list[EmployeeData]): Preprocessed employee data
            containing employee skills, proficiency levels, and maximum
            working hours.
        tasks_data (list[TaskData]): Preprocessed task data containing
            required skills, required proficiency levels, and task hours.
        population_size (int): Number of chromosomes in the population.
        generations (int): Number of generations to run.
        mutation_rate (int): Mutation probability as a percentage [0, 100].
        tournament_size (int): Number of chromosomes participating in
            each tournament.
        elite_size (int): Number of best chromosomes preserved between
            generations.

    Returns:
        tuple[list[list[int]], list[list[float | list[float] | list[int]]]]:
            The final population and the best solution information from each
            generation. Each generation stores the total cost, detailed costs,
            and the best chromosome in the following structure:

            [total_cost, detailed_costs, best_chromosome]

            The detailed costs contain skill mismatch, overtime, workload
            imbalance, and proficiency costs.
    """

    population = populate(population_size, len(tasks_data), len(employees_data))

    generations_best_costs = []

    for generation in range(generations):
        costs = cost(population, employees_data, tasks_data)

        best_index = costs[0].index(min(costs[0]))

        generations_best_costs.append(
            [costs[0][best_index], costs[1][best_index], population[best_index].copy()]
        )

        indices = list(range(len(costs[0])))
        indices.sort(key=lambda i: costs[0][i])

        elite_indices = indices[:elite_size]

        parent_indices = selection(
            costs[0], population_size - elite_size, tournament_size
        )

        parents = [population[i] for i in parent_indices]

        new_population = crossover(parents, crossover_type)

        new_population = mutate_population(
            new_population, mutation_rate, len(employees_data)
        )

        new_population += [population[i].copy() for i in elite_indices]

        population = new_population

    return population, generations_best_costs
