from pandas import DataFrame


EmployeeData = dict[str, int | str]
TaskData = dict[str, int | str | dict[str, int]]


def preprocess_employees(
    employees: DataFrame
) -> list[EmployeeData]:
    """
    Convert employee data from a DataFrame into GA-friendly dictionaries.

    Each employee's skills are parsed from the CSV string format into
    individual skill-level entries. Availability and employee name are
    also included in the resulting dictionary.

    Args:
        employees (DataFrame): DataFrame containing employee information.

    Returns:
        list[EmployeeData]: Preprocessed employee data containing skills,
        proficiency levels, available hours, and employee names.
    """

    employees_data = []

    for employee_id in range(employees.shape[0]):
        data = {}

        for skill in employees.loc[employee_id, "skills"].split(","):
            skill_name, level = skill.strip().split(":")
            data[skill_name] = int(level)

        data["available_hours"] = int(
            employees.loc[employee_id, "available_hours"]
        )
        data["name"] = employees.loc[employee_id, "name"]

        employees_data.append(data)

    return employees_data


def preprocess_tasks(
    tasks: DataFrame
) -> list[TaskData]:
    """
    Convert task data from a DataFrame into GA-friendly dictionaries.

    Required skills are parsed from the CSV string format into a
    dictionary mapping each required skill to its proficiency level.

    Args:
        tasks (DataFrame): DataFrame containing task information.

    Returns:
        list[TaskData]: Preprocessed task data containing task details,
        required skills, hours, and priority.
    """

    tasks_data = []

    for task_id in range(tasks.shape[0]):
        task_skills = {}

        for skill in tasks.loc[task_id, "required_skills"].split(","):
            skill_name, level = skill.strip().split(":")
            task_skills[skill_name] = int(level)

        data = {
            "task_id": tasks.loc[task_id, "task_id"],
            "task": tasks.loc[task_id, "task"],
            "required_skills": task_skills,
            "hours": int(tasks.loc[task_id, "hours"]),
            "priority": int(tasks.loc[task_id, "priority"])
        }

        tasks_data.append(data)

    return tasks_data