from src.chromosome import populate
from src.fitness import cost
from src.selection import selection
from src.crossover import crossover
from src.mutation import mutate_population
from src.data_loader import load_data


# from chromosome import populate
# from fitness import calculate_fitness
# from selection import selection
# from crossover import crossover
# from mutation import mutate_population
# from data_loader import load_data


def genetic_algorithm(employees, tasks, population_size, generations, mutation_rate, tournament_size, elite_size):



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

