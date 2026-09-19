from csv import DictWriter
from pathlib import Path
from time import perf_counter

from src import genetic_algorithm
from src.preprocessing import EmployeeData, TaskData


def save_results(results: list[dict], output_dir: Path) -> None:
    """
    Save experiment results to a CSV file.

    Args:
        results (list[dict]): Experiment result rows.
        output_dir (Path): Directory for the current experiment.

    Returns:
        None
    """

    file_path = output_dir / "results.csv"

    with file_path.open("w", newline="", encoding="utf-8") as file:
        writer = DictWriter(file, fieldnames=results[0].keys())

        writer.writeheader()
        writer.writerows(results)


def get_best_result(generations_best_costs: list) -> tuple[int, float, list[float]]:
    """
    Extract the best generation and its cost information.

    Args:
        generations_best_costs (list): Best result from each generation.

    Returns:
        tuple[int, float, list[float]]:
            Best generation index, total cost, and detailed costs.
    """

    best_generation = min(
        range(len(generations_best_costs)), key=lambda i: generations_best_costs[i][0]
    )

    best_result = generations_best_costs[best_generation]

    best_cost = best_result[0]
    detailed_costs = best_result[1]

    return (best_generation, best_cost, detailed_costs)


def run_experiment(
    employees_data: list[EmployeeData],
    tasks_data: list[TaskData],
    population_size: int | list[int],
    generations: int | list[int],
    mutation_rate: int | list[int],
    tournament_size: int | list[int],
    elite_size: int | list[int],
    crossover_type: str | list[str],
    RPT: int,
    output_dir: Path,
) -> list[dict]:

    parameters = {
        "population_size": population_size,
        "generations": generations,
        "mutation_rate": mutation_rate,
        "tournament_size": tournament_size,
        "elite_size": elite_size,
        "crossover_type": crossover_type,
    }

    # Find parameters that contain experiment values
    experiment_parameters = [
        parameter_name
        for parameter_name, parameter_value in parameters.items()
        if isinstance(parameter_value, list)
    ]

    # Multiple lists would require a grid search
    if len(experiment_parameters) > 1:
        raise ValueError("Only one parameter can be tested at a time.")

    # No lists -> test one complete configuration
    if len(experiment_parameters) == 0:
        experiment_parameter = "configuration"
        experiment_values = ["combined"]

    # One list -> compare its values
    else:
        experiment_parameter = experiment_parameters[0]
        experiment_values = parameters[experiment_parameter]

    results = []

    for experiment_value in experiment_values:
        # Create configuration for this experiment value
        current_parameters = parameters.copy()

        # Only replace a parameter when actually testing one
        if experiment_parameter != "configuration":
            current_parameters[experiment_parameter] = experiment_value

        for run_number in range(1, RPT + 1):
            start = perf_counter()

            _, generations_best_costs = genetic_algorithm(
                employees_data,
                tasks_data,
                current_parameters["population_size"],
                current_parameters["generations"],
                current_parameters["mutation_rate"],
                current_parameters["tournament_size"],
                current_parameters["crossover_type"],
                current_parameters["elite_size"],
            )

            execution_time = perf_counter() - start

            (best_generation, best_cost, detailed_costs) = get_best_result(
                generations_best_costs
            )

            results.append(
                {
                    "experiment_parameter": experiment_parameter,
                    "experiment_value": experiment_value,
                    "run": run_number,
                    "population_size": current_parameters["population_size"],
                    "generations": current_parameters["generations"],
                    "mutation_rate": current_parameters["mutation_rate"],
                    "tournament_size": current_parameters["tournament_size"],
                    "elite_size": current_parameters["elite_size"],
                    "crossover_type": current_parameters["crossover_type"],
                    "best_generation": best_generation,
                    "total_cost": round(best_cost, 2),
                    "skill_mismatch_cost": round(detailed_costs[0], 2),
                    "overtime_cost": round(detailed_costs[1], 2),
                    "imbalance_cost": round(detailed_costs[2], 2),
                    "proficiency_cost": round(detailed_costs[3], 2),
                    "priority_cost": round(detailed_costs[4], 2),
                    "execution_time": round(execution_time, 3),
                }
            )

            print(
                f"{experiment_parameter}: "
                f"{experiment_value} | "
                f"Run: {run_number}/{RPT} | "
                f"Cost: {best_cost:.2f}"
            )

    save_results(results, output_dir)

    return results
