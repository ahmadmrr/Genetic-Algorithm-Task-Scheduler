from pathlib import Path

import matplotlib.pyplot as plt


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