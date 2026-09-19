from datetime import datetime
from pathlib import Path
from shutil import copy2

from experiments.experiment import run_experiment
from experiments.visualization import plot_experiment_results
from src import load_data, preprocess_employees, preprocess_tasks
from src.config import load_config

RESULTS_DIR = Path(__file__).parent / "results"


def create_experiment_directory(config: dict) -> Path:
    """
    Create a unique directory for the current experiment
    and save its configuration.
    """

    experiment_parameters = [
        parameter for parameter, value in config.items() if isinstance(value, list)
    ]

    # Multiple lists would require a grid search
    if len(experiment_parameters) > 1:
        raise ValueError("Only one experiment parameter can be a list.")

    # No lists -> testing one complete configuration
    if len(experiment_parameters) == 0:
        experiment_parameter = "configuration"

    # One list -> testing that parameter
    else:
        experiment_parameter = experiment_parameters[0]

    timestamp = datetime.now().strftime(  # noqa: DTZ005
        "%Y-%m-%d_%H-%M-%S"
    )

    output_dir = RESULTS_DIR / f"{experiment_parameter}_{timestamp}"

    output_dir.mkdir(parents=True, exist_ok=False)

    config_path = Path(__file__).parent.parent / "config" / "experiment.toml"

    copy2(config_path, output_dir / "experiment.toml")

    return output_dir


def main() -> None:

    # Load dataset
    employees = load_data("data/employees.csv")

    tasks = load_data("data/tasks.csv")

    # Preprocess dataset
    employees_data = preprocess_employees(employees)

    tasks_data = preprocess_tasks(tasks)

    # Load experiment configuration
    config = load_config("experiment.toml")

    # Create unique experiment directory
    output_dir = create_experiment_directory(config)

    # Run experiment
    results = run_experiment(
        employees_data=employees_data,
        tasks_data=tasks_data,
        population_size=config["population_size"],
        generations=config["generations"],
        mutation_rate=config["mutation_rate"],
        tournament_size=config["tournament_size"],
        elite_size=config["elite_size"],
        crossover_type=config["crossover_type"],
        RPT=config["runs"],
        output_dir=output_dir,
    )

    # Generate experiment visualizations
    plot_experiment_results(results, output_dir)


if __name__ == "__main__":
    main()
