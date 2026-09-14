from numpy.random import randint, choice


def one_point_crossover(
    parent1: list[int],
    parent2: list[int]
) -> tuple[list[int], list[int]]:
    """
    Perform one-point crossover between two parent chromosomes.

    A random crossover point is selected, and the genes after that
    point are exchanged between the two parents.

    Args:
        parent1 (list[int]): First parent chromosome.
        parent2 (list[int]): Second parent chromosome.

    Returns:
        tuple[list[int], list[int]]: Two child chromosomes produced
        by one-point crossover.
    """

    cut_index = randint(1, len(parent1) - 1)

    child1 = parent1.copy()
    child2 = parent2.copy()

    temp = child1[cut_index:].copy()

    child1[cut_index:] = child2[cut_index:]
    child2[cut_index:] = temp

    return child1, child2


def two_points_crossover(
    parent1: list[int],
    parent2: list[int]
) -> tuple[list[int], list[int]]:
    """
    Perform two-point crossover between two parent chromosomes.

    Two distinct crossover points are selected randomly. The genes
    between the two crossover points are exchanged between the parents.

    Args:
        parent1 (list[int]): First parent chromosome.
        parent2 (list[int]): Second parent chromosome.

    Returns:
        tuple[list[int], list[int]]: Two child chromosomes produced
        by two-point crossover.
    """

    child1 = parent1.copy()
    child2 = parent2.copy()

    valid_positions = list(range(1, len(parent1) - 1))
    cuts = choice(valid_positions, size=2, replace=False)
    cut1, cut2 = sorted(cuts)

    temp = child1[cut1:cut2].copy()

    child1[cut1:cut2] = child2[cut1:cut2]
    child2[cut1:cut2] = temp

    return child1, child2


def uniform_crossover(
    parent1: list[int],
    parent2: list[int]
) -> tuple[list[int], list[int]]:
    """
    Perform uniform crossover between two parent chromosomes.

    A random binary mask is generated for the chromosome. For each
    position where the mask value is 1, the corresponding genes are
    exchanged between the two children.

    Args:
        parent1 (list[int]): First parent chromosome.
        parent2 (list[int]): Second parent chromosome.

    Returns:
        tuple[list[int], list[int]]: Two child chromosomes produced
        by uniform crossover.
    """

    mask = randint(0, 2, size=len(parent1))

    child1 = parent1.copy()
    child2 = parent2.copy()

    for gene_index, gene_mask in enumerate(mask):
        if gene_mask == 1:
            child1[gene_index], child2[gene_index] = (
                child2[gene_index],
                child1[gene_index]
            )

    return child1, child2


def crossover(
    population: list[list[int]],
    crossover_type: str
) -> list[list[int]]:
    """
    Perform the selected crossover operation on a population.

    Parent chromosomes are processed in pairs. The specified crossover
    operator is applied to each pair to produce two child chromosomes.
    If the population size is odd, the final unpaired chromosome is copied
    directly to the new population without crossover.

    Supported crossover types:
        - "one_point"
        - "two_points"
        - "uniform"

    Args:
        population (list[list[int]]): Population of parent chromosomes.
        crossover_type (str): Crossover operator to apply.

    Returns:
        list[list[int]]: Population of child chromosomes with the same
            size as the parent population.

    Raises:
        ValueError: If the specified crossover type is not supported.
    """
    operators = {
        "one_point": one_point_crossover,
        "two_points": two_points_crossover,
        "uniform": uniform_crossover
    }

    if crossover_type not in operators:
        raise ValueError(
            f"Unsupported crossover operator: {crossover_type}"
        )

    operator = operators[crossover_type]

    new_population = []

    for i in range(0, len(population) - 1, 2):

        child1, child2 = operator(
            population[i],
            population[i + 1]
        )

        new_population.append(child1)
        new_population.append(child2)

    if len(population) % 2 != 0:
        new_population.append(
            population[-1].copy()
        )

    return new_population