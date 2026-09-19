from numpy.random import choice


def tournament_selection(costs: list[float], tournament_size: int) -> int:
    """
    Selects a chromosome index using tournament selection.

    Randomly selects a group of chromosomes and returns the index
    of the chromosome with the lowest cost.

    Args:
        costs (list[float]): Cost of each chromosome in the population.
        tournament_size (int): Number of chromosomes competing in the tournament.

    Returns:
        int: Index of the chromosome with the lowest cost in the tournament.
    """

    population_size = len(costs)
    choices = choice(population_size, tournament_size, replace=False)
    chosen_costs = [costs[i] for i in choices]

    return choices[chosen_costs.index(min(chosen_costs))]


def selection(
    costs: list[float], selection_size: int, tournament_size: int
) -> list[int]:
    """
    Selects multiple chromosome indices using tournament selection.

    Args:
        costs (list[float]): Cost of each chromosome in the population.
        selection_size (int): Number of chromosome indices to select.
        tournament_size (int): Number of chromosomes competing in each tournament.

    Returns:
        list[int]: Indices of the selected chromosomes.
    """

    return [tournament_selection(costs, tournament_size) for _ in range(selection_size)]
