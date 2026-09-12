from pathlib import Path
from src.fitness import EmployeeData, TaskData


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
            [skill mismatch, overtime, workload imbalance, proficiency].
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

        file.write("GENETIC ALGORITHM SCHEDULER - BEST SOLUTION\n")
        file.write("=" * 85 + "\n\n")

        file.write(f"Total Cost:           {best_cost:.2f}\n")
        file.write(f"Skill Mismatch Cost:  {detailed_costs[0]:.2f}\n")
        file.write(f"Overtime Cost:        {detailed_costs[1]:.2f}\n")
        file.write(f"Imbalance Cost:       {detailed_costs[2]:.2f}\n")
        file.write(f"Proficiency Cost:     {detailed_costs[3]:.2f}\n")

        # =========================
        # Employee Workload Summary
        # =========================

        file.write("\n\nEMPLOYEE WORKLOAD SUMMARY\n")
        file.write("=" * 85 + "\n")

        file.write(
            f"{'ID':<8}"
            f"{'Employee':<20}"
            f"{'Tasks':<10}"
            f"{'Workload':<15}"
            f"{'Max Hours':<12}"
            f"{'Remaining':<12}\n"
        )

        file.write("-" * 85 + "\n")

        for employee_id, employee in enumerate(employees_data):

            name = employee["name"]
            max_hours = employee["max_hours"]

            assigned_hours = workloads[employee_id]["hours"]
            assigned_tasks = workloads[employee_id]["tasks"]

            remaining_hours = max_hours - assigned_hours

            file.write(
                f"{employee_id:<8}"
                f"{name:<20}"
                f"{assigned_tasks:<10}"
                f"{assigned_hours:<15}"
                f"{max_hours:<12}"
                f"{remaining_hours:<12}\n"
            )

        # =========================
        # Task Assignment Summary
        # =========================

        file.write("\n\nTASK ASSIGNMENT SUMMARY\n")
        file.write("=" * 110 + "\n")

        file.write(
            f"{'Task ID':<10}"
            f"{'Task':<32}"
            f"{'Employee':<20}"
            f"{'Skill':<15}"
            f"{'Req Lv':<10}"
            f"{'Emp Lv':<10}"
            f"{'Hours':<8}\n"
        )

        file.write("-" * 110 + "\n")

        for task_index, employee_index in enumerate(best_chromosome):

            task = tasks_data[task_index]
            employee = employees_data[employee_index]

            task_id = task["task_id"]
            task_name = task["task"]

            required_skill = task["required_skill"]
            required_level = task["required_level"]
            hours = task["hours"]

            employee_name = employee["name"]

            employee_level = employee.get(required_skill, "-")

            file.write(
                f"{task_id:<10}"
                f"{task_name:<32}"
                f"{employee_name:<20}"
                f"{required_skill:<15}"
                f"{required_level:<10}"
                f"{employee_level:<10}"
                f"{hours:<8}\n"
            )