from src.preprocessing import EmployeeData, TaskData
from src.config import load_config

fitness_config = load_config("fitness.toml")


def skill_mismatch_cost(
    chromosome: list[int],
    employees_data: list[EmployeeData],
    tasks_data: list[TaskData]
) -> int:
    """
    Calculate the skill mismatch cost for a chromosome.

    Each task may require multiple skills. A penalty of 10 is added
    for every required skill that the assigned employee does not have.

    Args:
        chromosome (list[int]): Employee index assigned to each task.
        employees_data (list[EmployeeData]): Preprocessed employee data
            containing employee skills, proficiency levels, availability,
            and names.
        tasks_data (list[TaskData]): Preprocessed task data containing
            required skills, required proficiency levels, task hours,
            and priority.

    Returns:
        int: Total skill mismatch cost across all task assignments.
    """

    cost = 0

    for task_index, employee_index in enumerate(chromosome):

        for required_skill in tasks_data[task_index]["required_skills"]:

            if required_skill not in employees_data[employee_index]:
                cost += fitness_config["skill"]["mismatch_penalty"]

    return cost


def overtime_cost(
    chromosome: list[int],
    employees_data: list[EmployeeData],
    tasks_data: list[TaskData]
) -> int:
    """
    Calculate the overtime cost for a chromosome.

    The total task hours assigned to each employee are calculated.
    A penalty is added when an employee's assigned hours exceed their
    available working hours.

    Args:
        chromosome (list[int]): Employee index assigned to each task.
        employees_data (list[EmployeeData]): Preprocessed employee data
            containing employee skills, proficiency levels, availability,
            and names.
        tasks_data (list[TaskData]): Preprocessed task data containing
            required skills, task hours, and priority.

    Returns:
        int: Total overtime cost across all employees.
    """

    cost = 0
    hours_map = {}

    for task_index, employee_index in enumerate(chromosome):
        if employee_index not in hours_map:
            hours_map[employee_index] = tasks_data[task_index]["hours"]
        else:
            hours_map[employee_index] += tasks_data[task_index]["hours"]

    for employee_id, hours_assigned in hours_map.items():
        available_hours = employees_data[employee_id]["available_hours"]

        if hours_assigned > available_hours:
            cost += (hours_assigned - available_hours) * fitness_config["overtime"]["penalty"]

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
            task information and assigned workload hours.
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
        cost += abs(hours - avg_hours) * fitness_config["workload_imbalance"]["weight"]

    return cost


def proficiency_cost(
    chromosome: list[int],
    employees_data: list[EmployeeData],
    tasks_data: list[TaskData]
) -> float:
    """
    Calculate the proficiency cost for a chromosome.

    Each task may require multiple skills. For every required skill
    possessed by the assigned employee, a penalty is calculated when
    the employee's proficiency level differs from the required level.

    Underqualification receives a larger penalty than overqualification.
    Missing skills are ignored because they are handled separately by
    the skill mismatch cost.

    Args:
        chromosome (list[int]): Employee index assigned to each task.
        employees_data (list[EmployeeData]): Preprocessed employee data
            containing employee skills and proficiency levels.
        tasks_data (list[TaskData]): Preprocessed task data containing
            required skills and their required proficiency levels.

    Returns:
        float: Total proficiency cost across all task assignments.
    """

    cost = 0.0

    for task_id, employee_id in enumerate(chromosome):

        required_skills = tasks_data[task_id]["required_skills"]

        for required_skill in required_skills:

            if required_skill in employees_data[employee_id]:

                required_level = required_skills[required_skill]
                employee_level = employees_data[employee_id][required_skill]

                # Underqualification cost
                if required_level > employee_level:
                    cost += (
                        required_level - employee_level
                    ) * fitness_config["proficiency"]["underqualification_penalty"]

                # Overqualification cost
                elif required_level < employee_level:
                    cost += (
                        employee_level - required_level
                    ) * fitness_config["proficiency"]["overqualification_penalty"]

    return cost


def priority_cost(
    chromosome: list[int],
    tasks_data: list[TaskData],
    employees_num: int
) -> float:
    """
    Calculate the priority imbalance cost among employees.

    Each task contributes a weighted priority load calculated by
    multiplying its priority by its working hours. The average priority
    load is calculated across all employees.

    Employees with a priority load above the average receive a stronger
    penalty of 0.5 per unit above the average. Employees below the
    average receive a smaller penalty of 0.1 per unit below the average.

    Employees with no assigned tasks are included with a priority load
    of zero.

    Args:
        chromosome (list[int]): Employee index assigned to each task.
        tasks_data (list[TaskData]): Preprocessed task data containing
            task hours and priority levels.
        employees_num (int): Total number of employees.

    Returns:
        float: Total priority imbalance cost across all employees.
    """

    total_priority_load = 0

    for task in tasks_data:
        total_priority_load += task["priority"] * task["hours"]

    avg_priority_load = total_priority_load / employees_num

    employees_priority_load = {
        employee_id: 0
        for employee_id in range(employees_num)
    }

    for task_index, employee_index in enumerate(chromosome):
        employees_priority_load[employee_index] += (
            tasks_data[task_index]["priority"]
            * tasks_data[task_index]["hours"]
        )

    cost = 0.0

    for employee_priority_load in employees_priority_load.values():

        # over average cost
        if employee_priority_load > avg_priority_load:
            cost += (
                employee_priority_load - avg_priority_load
            ) * fitness_config["priority"]["over_average_weight"]

        # under average cost
        elif employee_priority_load < avg_priority_load:
            cost += (
                avg_priority_load - employee_priority_load
            ) * fitness_config["priority"]["under_average_weight"]

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

        priority_cost_value = priority_cost(
            chromosome,
            tasks_data,
            len(employees_data)
        )

        total_cost = (
            skill_cost
            + overtime_cost_value
            + imbalance_cost_value
            + proficiency_cost_value
            + priority_cost_value
        )

        population_costs.append(total_cost)

        population_detailed_costs.append([
            skill_cost,
            overtime_cost_value,
            imbalance_cost_value,
            proficiency_cost_value,
            priority_cost_value
        ])

    return [population_costs, population_detailed_costs]