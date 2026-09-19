from src.crossover import (
    crossover,
    one_point_crossover,
    two_points_crossover,
    uniform_crossover,
)


def test_one_point_crossover():
    parent1 = [0, 0, 0, 0, 0]
    parent2 = [1, 1, 1, 1, 1]

    child1, child2 = one_point_crossover(
        parent1,
        parent2,
    )

    assert len(child1) == len(parent1)
    assert len(child2) == len(parent2)

    for gene1, gene2 in zip(child1, child2):
        assert {gene1, gene2} == {0, 1}


def test_two_points_crossover():
    parent1 = [0, 0, 0, 0, 0]
    parent2 = [1, 1, 1, 1, 1]

    child1, child2 = two_points_crossover(
        parent1,
        parent2,
    )

    assert len(child1) == len(parent1)
    assert len(child2) == len(parent2)

    for gene1, gene2 in zip(child1, child2):
        assert {gene1, gene2} == {0, 1}


def test_uniform_crossover():
    parent1 = [0, 0, 0, 0, 0]
    parent2 = [1, 1, 1, 1, 1]

    child1, child2 = uniform_crossover(
        parent1,
        parent2,
    )

    assert len(child1) == len(parent1)
    assert len(child2) == len(parent2)

    for gene1, gene2 in zip(child1, child2):
        assert {gene1, gene2} == {0, 1}


def test_crossover_odd_population():
    population = [
        [0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1],
        [2, 2, 2, 2, 2],
    ]

    new_population = crossover(
        population,
        "uniform",
    )

    assert len(new_population) == len(population)
    assert new_population[-1] == population[-1]
    assert new_population[-1] is not population[-1]
