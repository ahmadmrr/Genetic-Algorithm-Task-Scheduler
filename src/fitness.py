EmployeeData = dict[str, int | str]
TaskData = dict[str, str | int]


def skill_mismatch_cost(
    chromosome: list[int],
    employees_data: list[EmployeeData],
    tasks_data: list[TaskData]
) -> int:
    """
    Calculate the skill mismatch cost for a chromosome.

    A penalty is added whenever a task is assigned to an employee who
    does not have the skill required by that task.

    Args:
        chromosome (list[int]): Employee index assigned to each task.
        employees_data (list[EmployeeData]): Preprocessed employee data
            containing employee skills and maximum working hours.
        tasks_data (list[TaskData]): Preprocessed task data containing
            required skills, required levels, and task hours.

    Returns:
        int: Total skill mismatch cost.
    """

    cost = 0

    for task_index, employee_index in enumerate(chromosome):
        required_skill = tasks_data[task_index]["required_skill"]

        if required_skill not in employees_data[employee_index]:
            cost += 10

    return cost


def overtime_cost(
    chromosome: list[int],
    employees_data: list[EmployeeData],
    tasks_data: list[TaskData]
) -> int:
    """
    Calculate the overtime cost for a chromosome.

    The total task hours assigned to each employee are calculated.
    Employees whose assigned hours exceed their maximum working hours
    receive an overtime penalty.

    Args:
        chromosome (list[int]): Employee index assigned to each task.
        employees_data (list[EmployeeData]): Preprocessed employee data
            containing employee skills and maximum working hours.
        tasks_data (list[TaskData]): Preprocessed task data containing
            task hours and skill requirements.

    Returns:
        int: Total overtime cost.
    """

    cost = 0
    hours_map = {}

    for task_index, employee_index in enumerate(chromosome):
        if employee_index not in hours_map:
            hours_map[employee_index] = tasks_data[task_index]["hours"]
        else:
            hours_map[employee_index] += tasks_data[task_index]["hours"]

    for employee_id, hours_assigned in hours_map.items():
        max_hours = employees_data[employee_id]["max_hours"]

        if hours_assigned > max_hours:
            cost += (hours_assigned - max_hours) * 2

    return cost


def imbalance_cost(
    chromosome: list[int],
    tasks_data: list[TaskData],
    employees_num: int
) -> float:
    """
    Calculate the workload imbalance cost among employees.

    The assigned task hours for each employee are compared with the
    average workload. Greater deviations from the average produce a
    higher imbalance penalty.

    Employees with no assigned tasks are also included in the
    calculation with zero assigned hours.

    Args:
        chromosome (list[int]): Employee index assigned to each task.
        tasks_data (list[TaskData]): Preprocessed task data containing
            task hours and skill requirements.
        employees_num (int): Total number of employees.

    Returns:
        float: Total workload imbalance cost.
    """

    hours_map = {i: 0 for i in range(employees_num)}

    for task_index, employee_index in enumerate(chromosome):
        hours_map[employee_index] += tasks_data[task_index]["hours"]

    avg_hours = sum(hours_map.values()) / len(hours_map)

    cost = 0.0

    for hours in hours_map.values():
        cost += abs(hours - avg_hours) * 0.5

    return cost


def proficiency_cost(
    chromosome: list[int],
    employees_data: list[EmployeeData],
    tasks_data: list[TaskData]
) -> float:
    """
    Calculate the proficiency cost for a chromosome.

    Employees with the required skill receive a penalty when their
    proficiency level differs from the level required by the task.
    Underqualification receives a larger penalty than overqualification.

    Employees who do not have the required skill are ignored by this
    function because they are handled separately by the skill mismatch cost.

    Args:
        chromosome (list[int]): Employee index assigned to each task.
        employees_data (list[EmployeeData]): Preprocessed employee data
            containing employee skills and proficiency levels.
        tasks_data (list[TaskData]): Preprocessed task data containing
            required skills and required proficiency levels.

    Returns:
        float: Total proficiency cost.
    """

    cost = 0.0

    for task_id, employee_id in enumerate(chromosome):

        required_skill = tasks_data[task_id]["required_skill"]

        if required_skill in employees_data[employee_id]:

            required_level = tasks_data[task_id]["required_level"]
            employee_level = employees_data[employee_id][required_skill]

            # Underqualification cost
            if required_level > employee_level:
                cost += (required_level - employee_level) * 0.5

            # Overqualification cost
            elif required_level < employee_level:
                cost += (employee_level - required_level) * 0.1

    return cost


def cost(
    population: list[list[int]],
    employees_data: list[EmployeeData],
    tasks_data: list[TaskData]
) -> list[list[float] | list[list[float]]]:
    """
    Calculate the costs for all chromosomes in a population.

    For each chromosome, the skill mismatch, overtime, workload imbalance,
    and proficiency costs are calculated. These individual costs are then
    combined to produce the chromosome's total cost.

    Args:
        population (list[list[int]]): Population of chromosomes, where
            each chromosome represents task-to-employee assignments.
        employees_data (list[EmployeeData]): Preprocessed employee data
            containing employee skills, proficiency levels, and maximum
            working hours.
        tasks_data (list[TaskData]): Preprocessed task data containing
            required skills, required proficiency levels, and task hours.

    Returns:
        list[list[float] | list[list[float]]]: A list containing:
            - A list of total costs for each chromosome.
            - A list of detailed costs for each chromosome in the order:
              [skill mismatch, overtime, workload imbalance, proficiency].
    """

    population_costs = []
    population_detailed_costs = []

    for chromosome in population:
        skill_cost = skill_mismatch_cost(
            chromosome,
            employees_data,
            tasks_data
        )

        overtime_cost_value = overtime_cost(
            chromosome,
            employees_data,
            tasks_data
        )

        imbalance_cost_value = imbalance_cost(
            chromosome,
            tasks_data,
            len(employees_data)
        )

        proficiency_cost_value = proficiency_cost(
            chromosome,
            employees_data,
            tasks_data
        )

        total_cost = (
            skill_cost
            + overtime_cost_value
            + imbalance_cost_value
            + proficiency_cost_value
        )

        population_costs.append(total_cost)

        population_detailed_costs.append([
            skill_cost,
            overtime_cost_value,
            imbalance_cost_value,
            proficiency_cost_value
        ])

    return [population_costs, population_detailed_costs]