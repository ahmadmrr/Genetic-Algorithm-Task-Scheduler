from pathlib import Path
from .preprocessing import EmployeeData, TaskData


def _fit_text(text: str, width: int) -> str:
    """
    Fit text inside a fixed-width column.

    Text longer than the column width is truncated and ends with "...".
    """
    if len(text) <= width:
        return text

    return text[:width - 3] + "..."


def generate_report(
    best_chromosome: list[int],
    employees_data: list[EmployeeData],
    tasks_data: list[TaskData],
    best_cost: float,
    detailed_costs: list[float],
    output_path: str = "results/schedule_summary.txt"
) -> None:
    """
    Generate a text report for the best schedule found by the genetic algorithm.

    The report contains:
        - Overall cost summary
        - Employee workload summary
        - Task assignment summary

    Args:
        best_chromosome (list[int]): Best employee assignment for each task.
        employees_data (list[EmployeeData]): Preprocessed employee data.
        tasks_data (list[TaskData]): Preprocessed task data.
        best_cost (float): Total cost of the best chromosome.
        detailed_costs (list[float]): Individual cost components in the order:
            [
                skill mismatch,
                overtime,
                workload imbalance,
                proficiency,
                priority imbalance
            ].
        output_path (str): Path where the report will be saved.

    Returns:
        None
    """

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    workloads = {
        employee_id: {
            "hours": 0,
            "tasks": 0
        }
        for employee_id in range(len(employees_data))
    }

    for task_index, employee_id in enumerate(best_chromosome):
        workloads[employee_id]["hours"] += tasks_data[task_index]["hours"]
        workloads[employee_id]["tasks"] += 1

    with output_file.open("w", encoding="utf-8") as file:

        # =========================
        # Cost Summary
        # =========================

        file.write(
            "GENETIC ALGORITHM SCHEDULER - BEST SOLUTION\n"
        )
        file.write("=" * 120 + "\n\n")

        file.write(
            f"Total Cost:              {best_cost:.2f}\n"
        )
        file.write(
            f"Skill Mismatch Cost:     {detailed_costs[0]:.2f}\n"
        )
        file.write(
            f"Overtime Cost:           {detailed_costs[1]:.2f}\n"
        )
        file.write(
            f"Imbalance Cost:          {detailed_costs[2]:.2f}\n"
        )
        file.write(
            f"Proficiency Cost:        {detailed_costs[3]:.2f}\n"
        )
        file.write(
            f"Priority Imbalance Cost: {detailed_costs[4]:.2f}\n"
        )

        # =========================
        # Employee Workload Summary
        # =========================

        file.write("\n\nEMPLOYEE WORKLOAD SUMMARY\n")
        file.write("=" * 90 + "\n")

        file.write(
            f"{'ID':<6}"
            f"{'Employee':<20}"
            f"{'Tasks':<10}"
            f"{'Workload':<12}"
            f"{'Available':<12}"
            f"{'Remaining':<12}\n"
        )

        file.write("-" * 90 + "\n")

        for employee_id, employee in enumerate(employees_data):

            name = _fit_text(
                str(employee["name"]),
                18
            )

            available_hours = employee["available_hours"]
            assigned_hours = workloads[employee_id]["hours"]
            assigned_tasks = workloads[employee_id]["tasks"]

            remaining_hours = (
                available_hours - assigned_hours
            )

            file.write(
                f"{employee_id:<6}"
                f"{name:<20}"
                f"{assigned_tasks:<10}"
                f"{assigned_hours:<12}"
                f"{available_hours:<12}"
                f"{remaining_hours:<12}\n"
            )

        # =========================
        # Task Assignment Summary
        # =========================

        task_id_width = 10
        task_width = 32
        employee_width = 18
        required_skills_width = 34
        employee_levels_width = 34
        hours_width = 8
        priority_width = 10

        table_width = (
            task_id_width
            + task_width
            + employee_width
            + required_skills_width
            + employee_levels_width
            + hours_width
            + priority_width
        )

        file.write("\n\nTASK ASSIGNMENT SUMMARY\n")
        file.write("=" * table_width + "\n")

        file.write(
            f"{'Task ID':<{task_id_width}}"
            f"{'Task':<{task_width}}"
            f"{'Employee':<{employee_width}}"
            f"{'Required Skills':<{required_skills_width}}"
            f"{'Employee Levels':<{employee_levels_width}}"
            f"{'Hours':<{hours_width}}"
            f"{'Priority':<{priority_width}}\n"
        )

        file.write("-" * table_width + "\n")

        for task_index, employee_index in enumerate(best_chromosome):

            task = tasks_data[task_index]
            employee = employees_data[employee_index]

            task_id = str(task["task_id"])

            task_name = _fit_text(
                str(task["task"]),
                task_width - 2
            )

            employee_name = _fit_text(
                str(employee["name"]),
                employee_width - 2
            )

            required_skills = task["required_skills"]

            required_skills_text = ", ".join(
                f"{skill}:{level}"
                for skill, level in required_skills.items()
            )

            employee_levels_text = ", ".join(
                f"{skill}:{employee.get(skill, '-')}"
                for skill in required_skills
            )

            required_skills_text = _fit_text(
                required_skills_text,
                required_skills_width - 2
            )

            employee_levels_text = _fit_text(
                employee_levels_text,
                employee_levels_width - 2
            )

            hours = task["hours"]
            priority = task["priority"]

            file.write(
                f"{task_id:<{task_id_width}}"
                f"{task_name:<{task_width}}"
                f"{employee_name:<{employee_width}}"
                f"{required_skills_text:<{required_skills_width}}"
                f"{employee_levels_text:<{employee_levels_width}}"
                f"{hours:<{hours_width}}"
                f"{priority:<{priority_width}}\n"
            )