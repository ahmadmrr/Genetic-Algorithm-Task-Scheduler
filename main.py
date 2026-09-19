from time import perf_counter

from src import (
    generate_report,
    genetic_algorithm,
    load_data,
    preprocess_employees,
    preprocess_tasks,
)
from src.config import load_config
from src.plotting import (
    plot_cost_components,
    plot_employee_priority_load,
    plot_employee_workload,
    plot_total_cost,
)

ga_config = load_config("genetic_algorithm.toml")


# Genetic algorithm parameters
population_size = ga_config["population_size"]
generations = ga_config["generations"]
mutation_rate = ga_config["mutation_rate"]
tournament_size = ga_config["tournament_size"]
elite_size = ga_config["elite_size"]
crossover_type = ga_config["crossover_type"]


if __name__ == "__main__":
    # Load employee and task datasets
    employees = load_data("data/employees.csv")
    tasks = load_data("data/tasks.csv")

    # Data Preprocessing
    employees_data = preprocess_employees(employees)
    tasks_data = preprocess_tasks(tasks)

    start = perf_counter()

    # Run the genetic algorithm
    best_population, generations_best_costs = genetic_algorithm(
        employees_data,
        tasks_data,
        population_size,
        generations,
        mutation_rate,
        tournament_size,
        crossover_type,
        elite_size,
    )

    end = perf_counter()

    print(f"Execution time: {end - start:.3f} seconds")

    # Find the generation with the lowest total cost
    best_generation = min(
        range(len(generations_best_costs)), key=lambda i: generations_best_costs[i][0]
    )

    best_result = generations_best_costs[best_generation]

    best_cost = best_result[0]
    detailed_costs = best_result[1]
    best_chromosome = best_result[2]

    generate_report(
        best_chromosome, employees_data, tasks_data, best_cost, detailed_costs
    )

    print(
        f"\nGeneration {best_generation}\n"
        f"{'-' * 30}\n"
        f"Total Cost:          {best_cost:.2f}\n"
        f"Skill Mismatch Cost: {detailed_costs[0]:.2f}\n"
        f"Overtime Cost:       {detailed_costs[1]:.2f}\n"
        f"Imbalance Cost:      {detailed_costs[2]:.2f}\n"
        f"Proficiency Cost:    {detailed_costs[3]:.2f}\n"
        f"Priority Cost:       {detailed_costs[4]:.2f}\n"
        f"{'-' * 30}"
    )

    plot_total_cost(generations_best_costs, save_path="results/plots/total_cost.png")

    plot_cost_components(
        generations_best_costs, save_path="results/plots/cost_components.png"
    )

    plot_employee_workload(
        best_chromosome,
        employees_data,
        tasks_data,
        save_path="results/plots/employee_workload.png",
    )

    plot_employee_priority_load(
        best_chromosome,
        employees_data,
        tasks_data,
        save_path="results/plots/employee_priority_load.png",
    )
