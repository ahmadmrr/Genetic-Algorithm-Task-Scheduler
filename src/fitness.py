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


def imbalance_cost(
    chromosome: list[int],
    tasks: DataFrame,
    employees_num: int
) -> float:

    """
    Calculates the workload imbalance cost among employees.

    The total assigned task hours for each employee are compared to the
    average workload. Larger differences from the average produce a
    higher penalty.

    Args:
        chromosome (list[int]): Employee index assigned to each task.
        tasks (DataFrame): DataFrame containing task information and hours.
        employees_num (int): Total number of employees.

    Returns:
        float: The workload imbalance cost.
    """

    hours_map = {i: 0 for i in range(employees_num)}

    for task_index, employee_index in enumerate(chromosome):
        hours_map[employee_index] += tasks.loc[task_index, "hours"]

    avg_hours = sum(hours_map.values()) / len(hours_map)

    cost = 0
    for hours in hours_map.values():
        cost += abs(hours - avg_hours) * 0.5

    return cost


def cost(population : list[list[int]], employees : DataFrame, tasks : DataFrame) -> list[list[float] | list[list[float]]]:

    """    
    Calculate the total cost for a population of chromosomes.
    
    Args:
        population (list[list[int]]): A list of chromosomes representing task assignments.
        employees (DataFrame): DataFrame containing employee information.
        tasks (DataFrame): DataFrame containing task information.
            
    Returns:
        list[list[float] | list[list[float]]]: A list containing:
            - A list of total costs for each chromosome.
            - A list of detailed costs for each chromosome, where each
              inner list contains the skill mismatch, overtime, and
              workload imbalance costs."""

    costs = []
    population_costs = []
    population_detailed_costs = []
    for chromosome in population:

        skill_Cost = skill_mismatch_cost(chromosome, employees.copy(), tasks.copy())
        overtime_Cost = overtime_cost(chromosome, employees.copy(), tasks.copy())
        imbalance_Cost = imbalance_cost(chromosome, tasks.copy(), len(employees))

        population_costs.append(skill_Cost + overtime_Cost + imbalance_Cost)
        population_detailed_costs.append([skill_Cost, overtime_Cost, imbalance_Cost])
    
    return [population_costs, population_detailed_costs]