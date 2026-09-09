import numpy as np

def chromosome(num_tasks, num_employees):
    return np.random.randint(0, num_employees, size=num_tasks)


def populate(population_size, num_tasks, num_employees):
    return np.array([chromosome(num_tasks, num_employees) for _ in range(population_size)])

