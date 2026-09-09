import random


def chromosome(num_tasks: int, num_employees: int) -> list[int]:
    """
    Generates a random chromosome for task assignment.

    Args:
        num_tasks (int): Number of tasks.
        num_employees (int): Number of available employees.

    Returns:
        list[int]: Employee indices assigned to each task, 
        ranging from 0 to num_employees - 1.
    """

    return [
        random.randrange(num_employees)
        for _ in range(num_tasks)
    ]


def populate(
    population_size: int,
    num_tasks: int,
    num_employees: int
) -> list[list[int]]:
    """
    Generates an initial population of random chromosomes.

    Args:
        population_size (int): Number of chromosomes.
        num_tasks (int): Number of tasks.
        num_employees (int): Number of available employees.

    Returns:
        list[list[int]]: The generated population.
    """

    return [
        chromosome(num_tasks, num_employees)
        for _ in range(population_size)
    ]