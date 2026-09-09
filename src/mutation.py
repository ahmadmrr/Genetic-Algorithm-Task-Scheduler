from numpy.random import randint, random


def mutate(chromosome : list[int], mutation_rate: int, employees_number: int) -> list[int]:

    """
    Mutates a chromosome by randomly changing employee assignments.

    Each gene has a chance to mutate based on the mutation rate.
    When mutated, a different employee is assigned to the task.

    Args:
        chromosome (list[int]): Chromosome containing employee assignments.
        mutation_rate (int): Mutation probability for each gene as a percentage [0, 100].
        employees_number (int): Number of available employees.

    Returns:
        list[int]: The mutated chromosome.
    """

    for i in range(len(chromosome)):

        probability = random()

        if probability < (mutation_rate/100):

            new_employee = randint(0, employees_number)

            # Prevent mutation from selecting the same employee
            while new_employee == chromosome[i]:
                new_employee = randint(0, employees_number)

            chromosome[i] = new_employee

    return chromosome


def mutate_population(population: list[list[int]], mutation_rate: int, employees_number: int) -> list[list[int]]:

    """
    Applies mutation to every chromosome in the population.

    Args:
        population (list[list[int]]): Population of chromosomes.
        mutation_rate (int): Mutation probability for each gene as a percentage [0, 100].
        employees_number (int): Number of available employees.

    Returns:
        list[list[int]]: The mutated population.
    """

    for i in range(len(population)):
        population[i] = mutate(population[i], mutation_rate, employees_number)

    return population
