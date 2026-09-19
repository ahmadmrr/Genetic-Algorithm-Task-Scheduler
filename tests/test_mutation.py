from src.mutation import mutate, mutate_population


def test_mutate_zero_rate():
    chromosome = [0, 1, 2, 3, 4]

    mutated = mutate(
        chromosome.copy(),
        0,
        5,
    )

    assert mutated == chromosome


def test_mutation_keeps_valid_employees():
    chromosome = [0, 0, 0, 0, 0]

    mutated = mutate(
        chromosome.copy(),
        100,
        5,
    )

    assert len(mutated) == len(chromosome)

    for employee_index in mutated:
        assert 0 <= employee_index < 5


def test_mutate_population_size():
    population = [
        [0, 1, 2],
        [2, 1, 0],
        [1, 2, 0],
    ]

    mutated_population = mutate_population(
        population,
        0,
        3,
    )

    assert len(mutated_population) == len(population)


def test_mutate_population_zero_rate():
    population = [
        [0, 1, 2],
        [2, 1, 0],
    ]

    original = [chromosome.copy() for chromosome in population]

    mutated_population = mutate_population(
        population,
        0,
        3,
    )

    assert mutated_population == original
