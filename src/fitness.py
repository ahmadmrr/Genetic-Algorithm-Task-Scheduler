from pandas import DataFrame


def skill_mismatch_cost(chromosome : list[int], employees : DataFrame, tasks : DataFrame) -> int:

    """
    Calculate the skill mismatch cost for a given chromosome.

    Args:
        chromosome (list[int]): The chromosome representing task assignments.
        employees (DataFrame): DataFrame containing employee information.
        tasks (DataFrame): DataFrame containing task information.

    Returns:
        int: The skill mismatch cost.
    """

    cost = 0
    for i, j in enumerate(chromosome):
        if tasks.loc[i, 'required_skill'] in employees.loc[j, 'skills']:
            continue
        else:
            cost += 10
    return cost


def overtime_cost(chromosome : list[int], employees : DataFrame, tasks : DataFrame) -> int:

    """
    Calculate the overtime cost for a given chromosome.

    Args:
        chromosome (list[int]): The chromosome representing task assignments.
        employees (DataFrame): DataFrame containing employee information.
        tasks (DataFrame): DataFrame containing task information.

    Returns:
        int: The overtime cost.
    """

    cost = 0
    hours_map = {}
    for i, j in enumerate(chromosome):
        if j not in hours_map.keys():
            hours_map[j] = tasks.loc[i, 'hours']
        else:
            hours_map[j] += tasks.loc[i, 'hours']

    for key, value in hours_map.items():
        if value > employees.loc[key, 'max_hours']:
            cost += (value - employees.loc[key, 'max_hours']) * 2
    return cost


def cost(population : list[list[int]], employees : DataFrame, tasks : DataFrame) -> list[int]:

    """    
    Calculate the total cost for a population of chromosomes.
    
    Args:
        population (list[list[int]]): A list of chromosomes representing task assignments.
        employees (DataFrame): DataFrame containing employee information.
        tasks (DataFrame): DataFrame containing task information.
            
    Returns:
        list[int]: A list of total costs for each chromosome in the population."""

    costs = []

    for chromosome in population:

        skill_cost = skill_mismatch_cost(chromosome, employees.copy(), tasks.copy())
        overtime = overtime_cost(chromosome, employees.copy(), tasks.copy())
        costs.append(skill_cost + overtime)
    
    return costs

