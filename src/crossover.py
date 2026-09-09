from numpy.random import randint


def one_paire_crossover(parent1, parent2, cut_index):\

    child1 = parent1.copy()
    child2 = parent2.copy()

    temp = child1[cut_index:].copy()

    child1[cut_index:] = child2[cut_index:]
    child2[cut_index:] = temp

    return child1, child2


def crossover(population):

    new_population = []

    for i in range(0, len(population), 2):
        cut_index = randint(1, len(population[i]))
        parent1, parent2 = one_paire_crossover(population[i], population[i + 1], cut_index)
        new_population.append(parent1)
        new_population.append(parent2)

    return new_population
