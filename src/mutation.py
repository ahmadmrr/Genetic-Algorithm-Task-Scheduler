from numpy.random import randint, random


def mutate(chromosome, mutation_rate, employees_number):

    for i in range(len(chromosome)):

        probability = random()

        if probability < (mutation_rate/100):

            new_employee = randint(0, employees_number)
            while new_employee == chromosome[i]:
                new_employee = randint(0, employees_number)
            chromosome[i] = new_employee

    return chromosome


def mutate_population(population, mutation_rate, employees_number):

    for i in range(len(population)):
        population[i] = mutate(population[i], mutation_rate, employees_number)

    return population
