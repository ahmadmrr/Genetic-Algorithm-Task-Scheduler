from numpy.random import choice


def tournament_selection(costs, tournament_size):

    population_size = len(costs)
    choices = choice(population_size, tournament_size, replace=False)
    chosen_costs = [costs[i] for i in choices]

    return choices[chosen_costs.index(min(chosen_costs))]


def selection(costs, selection_size, tournament_size):

    return [tournament_selection(costs, tournament_size) for _ in range(selection_size)]


