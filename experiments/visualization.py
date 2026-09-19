from pathlib import Path

import matplotlib.pyplot as plt

COST_COMPONENTS = [
    "skill_mismatch_cost",
    "overtime_cost",
    "imbalance_cost",
    "proficiency_cost",
    "priority_cost",
]


def _save_plot(file_name: str, output_dir: Path, show: bool) -> None:
    """
    Save the current plot inside the experiment output directory.

    Args:
        file_name (str): Name of the output image file.
        output_dir (Path): Directory for the current experiment.
        show (bool): Whether to display the plot.
    """

    plots_dir = output_dir / "plots"

    plots_dir.mkdir(parents=True, exist_ok=True)

    plt.savefig(plots_dir / file_name, bbox_inches="tight", dpi=300)

    if show:
        plt.show()

    plt.close()


def _validate_results(results: list[dict]) -> None:
    """
    Validate that experiment results are available.

    Args:
        results (list[dict]): Experiment result rows.

    Raises:
        ValueError: If the results list is empty.
    """

    if not results:
        raise ValueError("Experiment results cannot be empty.")


def _group_results(results: list[dict], metric: str) -> dict:
    """
    Group a result metric by experiment value.

    Args:
        results (list[dict]): Experiment result rows.
        metric (str): Result column to group.

    Returns:
        dict: Experiment values mapped to metric values.
    """

    grouped = {}

    for result in results:
        experiment_value = result["experiment_value"]

        if experiment_value not in grouped:
            grouped[experiment_value] = []

        grouped[experiment_value].append(result[metric])

    return grouped


def _format_parameter(parameter: str) -> str:
    """
    Convert a parameter name into a readable label.
    """

    return parameter.replace("_", " ").title()


# ============================================================
# PARAMETER COMPARISON PLOTS
# ============================================================


def plot_average_cost(results: list[dict], output_dir: Path, show: bool = True) -> None:
    """
    Plot the average total cost for each tested value.
    """

    _validate_results(results)

    experiment_parameter = results[0]["experiment_parameter"]

    grouped = _group_results(results, "total_cost")

    values = list(grouped.keys())

    averages = [sum(costs) / len(costs) for costs in grouped.values()]

    plt.figure(figsize=(9, 5))

    plt.bar([str(value) for value in values], averages)

    plt.xlabel(_format_parameter(experiment_parameter))

    plt.ylabel("Average Total Cost")

    plt.title(f"Average Cost by {_format_parameter(experiment_parameter)}")

    plt.grid(axis="y", alpha=0.3)

    _save_plot(f"{experiment_parameter}_average_cost.png", output_dir, show)


def plot_cost_distribution(
    results: list[dict], output_dir: Path, show: bool = True
) -> None:
    """
    Plot the distribution of total costs for each tested value.
    """

    _validate_results(results)

    experiment_parameter = results[0]["experiment_parameter"]

    grouped = _group_results(results, "total_cost")

    values = list(grouped.keys())
    costs = list(grouped.values())

    plt.figure(figsize=(9, 5))

    plt.boxplot(costs, tick_labels=[str(value) for value in values])

    plt.xlabel(_format_parameter(experiment_parameter))

    plt.ylabel("Total Cost")

    plt.title(f"Cost Distribution by {_format_parameter(experiment_parameter)}")

    plt.grid(axis="y", alpha=0.3)

    _save_plot(f"{experiment_parameter}_cost_distribution.png", output_dir, show)


def plot_average_execution_time(
    results: list[dict], output_dir: Path, show: bool = True
) -> None:
    """
    Plot the average execution time for each tested value.
    """

    _validate_results(results)

    experiment_parameter = results[0]["experiment_parameter"]

    grouped = _group_results(results, "execution_time")

    values = list(grouped.keys())

    averages = [sum(times) / len(times) for times in grouped.values()]

    plt.figure(figsize=(9, 5))

    plt.bar([str(value) for value in values], averages)

    plt.xlabel(_format_parameter(experiment_parameter))

    plt.ylabel("Average Execution Time (seconds)")

    plt.title(f"Execution Time by {_format_parameter(experiment_parameter)}")

    plt.grid(axis="y", alpha=0.3)

    _save_plot(f"{experiment_parameter}_execution_time.png", output_dir, show)


def plot_average_cost_components(
    results: list[dict], output_dir: Path, show: bool = True
) -> None:
    """
    Plot the average fitness cost components for each tested value.
    """

    _validate_results(results)

    experiment_parameter = results[0]["experiment_parameter"]

    experiment_values = list(
        dict.fromkeys(result["experiment_value"] for result in results)
    )

    component_averages = {}

    for component in COST_COMPONENTS:
        grouped = _group_results(results, component)

        component_averages[component] = [
            sum(grouped[value]) / len(grouped[value]) for value in experiment_values
        ]

    x_positions = list(range(len(experiment_values)))

    number_of_components = len(COST_COMPONENTS)

    group_width = 0.8
    bar_width = group_width / number_of_components

    plt.figure(figsize=(11, 6))

    for component_index, component in enumerate(COST_COMPONENTS):
        offset = (component_index - (number_of_components - 1) / 2) * bar_width

        positions = [x + offset for x in x_positions]

        label = component.replace("_cost", "").replace("_", " ").title()

        plt.bar(positions, component_averages[component], width=bar_width, label=label)

    plt.xticks(x_positions, [str(value) for value in experiment_values])

    plt.xlabel(_format_parameter(experiment_parameter))

    plt.ylabel("Average Cost")

    plt.title(f"Average Cost Components by {_format_parameter(experiment_parameter)}")

    plt.legend()

    plt.grid(axis="y", alpha=0.3)

    _save_plot(f"{experiment_parameter}_cost_components.png", output_dir, show)


def plot_constraint_satisfaction_rates(
    results: list[dict], output_dir: Path, show: bool = True
) -> None:
    """
    Plot constraint satisfaction rates for each tested value.

    No skill mismatch:
        skill_mismatch_cost == 0

    No overtime:
        overtime_cost == 0

    Both constraints satisfied:
        skill_mismatch_cost == 0
        and overtime_cost == 0
    """

    _validate_results(results)

    experiment_parameter = results[0]["experiment_parameter"]

    experiment_values = list(
        dict.fromkeys(result["experiment_value"] for result in results)
    )

    no_skill_mismatch_rates = []
    no_overtime_rates = []
    both_satisfied_rates = []

    for value in experiment_values:
        value_results = [
            result for result in results if result["experiment_value"] == value
        ]

        total_runs = len(value_results)

        no_skill_mismatch = sum(
            result["skill_mismatch_cost"] == 0 for result in value_results
        )

        no_overtime = sum(result["overtime_cost"] == 0 for result in value_results)

        both_satisfied = sum(
            result["skill_mismatch_cost"] == 0 and result["overtime_cost"] == 0
            for result in value_results
        )

        no_skill_mismatch_rates.append(no_skill_mismatch / total_runs * 100)

        no_overtime_rates.append(no_overtime / total_runs * 100)

        both_satisfied_rates.append(both_satisfied / total_runs * 100)

    x_positions = list(range(len(experiment_values)))

    bar_width = 0.25

    plt.figure(figsize=(10, 6))

    plt.bar(
        [x - bar_width for x in x_positions],
        no_skill_mismatch_rates,
        width=bar_width,
        label="No Skill Mismatch",
    )

    plt.bar(x_positions, no_overtime_rates, width=bar_width, label="No Overtime")

    plt.bar(
        [x + bar_width for x in x_positions],
        both_satisfied_rates,
        width=bar_width,
        label="Both Satisfied",
    )

    plt.xticks(x_positions, [str(value) for value in experiment_values])

    plt.ylim(0, 100)

    plt.xlabel(_format_parameter(experiment_parameter))

    plt.ylabel("Runs Satisfying Constraint (%)")

    plt.title(
        f"Constraint Satisfaction Rates by {_format_parameter(experiment_parameter)}"
    )

    plt.legend()

    plt.grid(axis="y", alpha=0.3)

    _save_plot(f"{experiment_parameter}_constraint_satisfaction.png", output_dir, show)


# ============================================================
# CONFIGURATION TEST PLOTS
# ============================================================


def plot_configuration_costs(
    results: list[dict], output_dir: Path, show: bool = True
) -> None:
    """
    Plot the total cost produced by each configuration run.
    """

    _validate_results(results)

    runs = [result["run"] for result in results]

    costs = [result["total_cost"] for result in results]

    average_cost = sum(costs) / len(costs)

    plt.figure(figsize=(10, 5))

    plt.plot(runs, costs, marker="o", label="Total Cost")

    plt.axhline(average_cost, linestyle="--", label=f"Average ({average_cost:.2f})")

    plt.xlabel("Run")
    plt.ylabel("Total Cost")

    plt.title("Combined Configuration - Cost Across Runs")

    plt.legend()

    plt.grid(alpha=0.3)

    _save_plot("configuration_costs.png", output_dir, show)


def plot_configuration_distribution(
    results: list[dict], output_dir: Path, show: bool = True
) -> None:
    """
    Plot the distribution of total costs across configuration runs.
    """

    _validate_results(results)

    costs = [result["total_cost"] for result in results]

    plt.figure(figsize=(6, 5))

    plt.boxplot(costs, tick_labels=["Combined"])

    plt.ylabel("Total Cost")

    plt.title("Combined Configuration - Cost Distribution")

    plt.grid(axis="y", alpha=0.3)

    _save_plot("configuration_cost_distribution.png", output_dir, show)


def plot_configuration_cost_components(
    results: list[dict], output_dir: Path, show: bool = True
) -> None:
    """
    Plot the average fitness cost components
    across configuration runs.
    """

    _validate_results(results)

    component_averages = []

    for component in COST_COMPONENTS:
        average = sum(result[component] for result in results) / len(results)

        component_averages.append(average)

    labels = [
        component.replace("_cost", "").replace("_", " ").title()
        for component in COST_COMPONENTS
    ]

    plt.figure(figsize=(9, 5))

    plt.bar(labels, component_averages)

    plt.ylabel("Average Cost")

    plt.title("Combined Configuration - Average Cost Components")

    plt.xticks(rotation=20)

    plt.grid(axis="y", alpha=0.3)

    _save_plot("configuration_cost_components.png", output_dir, show)


# ============================================================
# MAIN VISUALIZATION FUNCTION
# ============================================================


def plot_experiment_results(
    results: list[dict], output_dir: Path, show: bool = True
) -> None:
    """
    Generate visualizations based on the experiment type.

    Parameter comparison:
        1. Average total cost
        2. Cost distribution
        3. Average cost components
        4. Constraint satisfaction rates
        5. Average execution time

    Configuration test:
        1. Cost across runs
        2. Cost distribution
        3. Average cost components
    """

    _validate_results(results)

    experiment_parameter = results[0]["experiment_parameter"]

    if experiment_parameter == "configuration":
        plot_configuration_costs(results, output_dir, show)

        plot_configuration_distribution(results, output_dir, show)

        plot_configuration_cost_components(results, output_dir, show)

        return

    plot_average_cost(results, output_dir, show)

    plot_cost_distribution(results, output_dir, show)

    plot_average_cost_components(results, output_dir, show)

    plot_constraint_satisfaction_rates(results, output_dir, show)

    plot_average_execution_time(results, output_dir, show)
