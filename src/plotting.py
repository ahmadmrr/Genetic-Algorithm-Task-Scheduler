from pathlib import Path
import matplotlib.pyplot as plt
from .preprocessing import TaskData, EmployeeData

def _save_plot(save_path: str | None) -> None:
    """
    Save the current plot if a save path is provided.

    Args:
        save_path (str | None): Path where the plot should be saved.
    """

    if save_path is None:
        return

    output_path = Path(save_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.savefig(
        output_path,
        bbox_inches="tight",
        dpi=300
    )


def plot_total_cost(
    generations_best_costs: list,
    title: str = "GA Convergence",
    save_path: str | None = None,
    show: bool = True
) -> None:
    """
    Plot the best total cost for each generation.

    Args:
        generations_best_costs (list): Best solution data stored for
            each generation.
        title (str): Plot title.
        save_path (str | None): Optional path used to save the plot.
        show (bool): Whether to display the plot.

    Returns:
        None
    """

    total_costs = [
        generation[0]
        for generation in generations_best_costs
    ]

    generations = range(len(total_costs))

    plt.figure(figsize=(10, 6))

    plt.plot(
        generations,
        total_costs,
        label="Total Cost"
    )

    plt.xlabel("Generation")
    plt.ylabel("Cost")
    plt.title(title)

    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()

    _save_plot(save_path)

    if show:
        plt.show()

    plt.close()


def plot_cost_components(
    generations_best_costs: list,
    title: str = "Cost Components by Generation",
    save_path: str | None = None,
    show: bool = True
) -> None:
    """
    Plot each fitness cost component across generations.

    The expected detailed cost order is:
        0 - Skill mismatch
        1 - Overtime
        2 - Workload imbalance
        3 - Proficiency
        4 - Priority imbalance

    Args:
        generations_best_costs (list): Best solution data stored for
            each generation.
        title (str): Plot title.
        save_path (str | None): Optional path used to save the plot.
        show (bool): Whether to display the plot.

    Returns:
        None
    """

    skill_costs = [
        generation[1][0]
        for generation in generations_best_costs
    ]

    overtime_costs = [
        generation[1][1]
        for generation in generations_best_costs
    ]

    imbalance_costs = [
        generation[1][2]
        for generation in generations_best_costs
    ]

    proficiency_costs = [
        generation[1][3]
        for generation in generations_best_costs
    ]

    priority_costs = [
        generation[1][4]
        for generation in generations_best_costs
    ]

    generations = range(len(generations_best_costs))

    plt.figure(figsize=(12, 7))

    plt.plot(
        generations,
        skill_costs,
        label="Skill Mismatch"
    )

    plt.plot(
        generations,
        overtime_costs,
        label="Overtime"
    )

    plt.plot(
        generations,
        imbalance_costs,
        label="Workload Imbalance"
    )

    plt.plot(
        generations,
        proficiency_costs,
        label="Proficiency"
    )

    plt.plot(
        generations,
        priority_costs,
        label="Priority Imbalance"
    )

    plt.xlabel("Generation")
    plt.ylabel("Cost")
    plt.title(title)

    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()

    _save_plot(save_path)

    if show:
        plt.show()

    plt.close()


def plot_all_costs(
    generations_best_costs: list,
    title: str = "Genetic Algorithm Performance",
    save_path: str | None = None,
    show: bool = True
) -> None:
    """
    Plot total cost and all individual fitness components together.

    Args:
        generations_best_costs (list): Best solution data stored for
            each generation.
        title (str): Plot title.
        save_path (str | None): Optional path used to save the plot.
        show (bool): Whether to display the plot.

    Returns:
        None
    """

    total_costs = [
        generation[0]
        for generation in generations_best_costs
    ]

    skill_costs = [
        generation[1][0]
        for generation in generations_best_costs
    ]

    overtime_costs = [
        generation[1][1]
        for generation in generations_best_costs
    ]

    imbalance_costs = [
        generation[1][2]
        for generation in generations_best_costs
    ]

    proficiency_costs = [
        generation[1][3]
        for generation in generations_best_costs
    ]

    priority_costs = [
        generation[1][4]
        for generation in generations_best_costs
    ]

    generations = range(len(generations_best_costs))

    plt.figure(figsize=(12, 7))

    plt.plot(
        generations,
        total_costs,
        label="Total Cost",
        linewidth=2
    )

    plt.plot(
        generations,
        skill_costs,
        label="Skill Mismatch"
    )

    plt.plot(
        generations,
        overtime_costs,
        label="Overtime"
    )

    plt.plot(
        generations,
        imbalance_costs,
        label="Workload Imbalance"
    )

    plt.plot(
        generations,
        proficiency_costs,
        label="Proficiency"
    )

    plt.plot(
        generations,
        priority_costs,
        label="Priority Imbalance"
    )

    plt.xlabel("Generation")
    plt.ylabel("Cost")
    plt.title(title)

    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()

    _save_plot(save_path)

    if show:
        plt.show()

    plt.close()


def plot_employee_workload(
    best_chromosome: list[int],
    employees_data: list[EmployeeData],
    tasks_data: list[TaskData],
    title: str = "Employee Workload",
    save_path: str | None = None,
    show: bool = True
) -> None:
    """
    Plot the total assigned working hours for each employee.

    Args:
        best_chromosome (list[int]): Best employee assignment for each task.
        employees_data (list[EmployeeData]): Preprocessed employee data.
        tasks_data (list[TaskData]): Preprocessed task data.
        title (str): Plot title.
        save_path (str | None): Optional path used to save the plot.
        show (bool): Whether to display the plot.

    Returns:
        None
    """

    employees_num = len(employees_data)

    workloads = {
        employee_id: 0
        for employee_id in range(employees_num)
    }

    for task_index, employee_index in enumerate(best_chromosome):
        workloads[employee_index] += tasks_data[task_index]["hours"]

    employee_names = [
        employees_data[employee_id]["name"]
        for employee_id in range(employees_num)
    ]

    assigned_hours = [
        workloads[employee_id]
        for employee_id in range(employees_num)
    ]

    available_hours = [
        employees_data[employee_id]["available_hours"]
        for employee_id in range(employees_num)
    ]

    positions = range(employees_num)

    plt.figure(figsize=(14, 7))

    plt.bar(
        positions,
        assigned_hours,
        label="Assigned Hours"
    )

    plt.plot(
        positions,
        available_hours,
        marker="o",
        label="Available Hours"
    )

    plt.xticks(
        positions,
        employee_names,
        rotation=45,
        ha="right"
    )

    plt.xlabel("Employee")
    plt.ylabel("Hours")
    plt.title(title)

    plt.grid(
        axis="y",
        alpha=0.3
    )

    plt.legend()
    plt.tight_layout()

    _save_plot(save_path)

    if show:
        plt.show()

    plt.close()


def plot_employee_priority_load(
    best_chromosome: list[int],
    employees_data: list[EmployeeData],
    tasks_data: list[TaskData],
    title: str = "Employee Priority Load",
    save_path: str | None = None,
    show: bool = True
) -> None:
    """
    Plot the weighted priority load assigned to each employee.

    Priority load is calculated as:

        task priority * task hours

    The average priority load across all employees is also displayed
    for comparison.

    Args:
        best_chromosome (list[int]): Best employee assignment for each task.
        employees_data (list[EmployeeData]): Preprocessed employee data.
        tasks_data (list[TaskData]): Preprocessed task data.
        title (str): Plot title.
        save_path (str | None): Optional path used to save the plot.
        show (bool): Whether to display the plot.

    Returns:
        None
    """

    employees_num = len(employees_data)

    priority_loads = {
        employee_id: 0
        for employee_id in range(employees_num)
    }

    for task_index, employee_index in enumerate(best_chromosome):

        task = tasks_data[task_index]

        priority_loads[employee_index] += (
            task["priority"] * task["hours"]
        )

    employee_names = [
        employees_data[employee_id]["name"]
        for employee_id in range(employees_num)
    ]

    loads = [
        priority_loads[employee_id]
        for employee_id in range(employees_num)
    ]

    avg_priority_load = sum(loads) / employees_num

    positions = range(employees_num)

    plt.figure(figsize=(14, 7))

    plt.bar(
        positions,
        loads,
        label="Priority Load"
    )

    plt.axhline(
        y=avg_priority_load,
        linestyle="--",
        label=f"Average Priority Load ({avg_priority_load:.2f})"
    )

    plt.xticks(
        positions,
        employee_names,
        rotation=45,
        ha="right"
    )

    plt.xlabel("Employee")
    plt.ylabel("Priority Load")
    plt.title(title)

    plt.grid(
        axis="y",
        alpha=0.3
    )

    plt.legend()
    plt.tight_layout()

    _save_plot(save_path)

    if show:
        plt.show()

    plt.close()