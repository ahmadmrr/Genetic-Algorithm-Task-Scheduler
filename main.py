from src import load_data, genetic_algorithm, generate_report
import matplotlib.pyplot as plt
from time import perf_counter


# Genetic algorithm parameters
population_size = 100
generations = 200
mutation_rate = 5
tournament_size = 5
elite_size = 2


if __name__ == "__main__":

    # Load employee and task datasets
    employees = load_data("data/employees.csv")
    tasks = load_data("data/tasks.csv")

    # Data Preprocessing

    employees_data = []
    for employee_id in range(employees.shape[0]):

        data = {}
        for skill in employees.loc[employee_id, 'skills'].split(','):

            skill_name, level = skill.strip().split(":")
            data[skill_name] = int(level)

        data['max_hours'] = int(employees.loc[employee_id, "max_hours"])
        data["name"] = employees.loc[employee_id, 'name']

        employees_data.append(data)


    tasks_data = []

    for task_id in range(tasks.shape[0]):
        data = {
            "task_id": tasks.loc[task_id, "task_id"],
            "task": tasks.loc[task_id, "task"],
            "required_skill": tasks.loc[task_id, "required_skill"],
            "required_level": int(tasks.loc[task_id, "required_level"]),
            "hours": int(tasks.loc[task_id, "hours"])
        }

        tasks_data.append(data)


    start = perf_counter()

    # Run the genetic algorithm
    best_population, generations_best_costs = genetic_algorithm(
        employees_data,
        tasks_data,
        population_size,
        generations,
        mutation_rate,
        tournament_size,
        elite_size
    )

    end = perf_counter()

    print(f"Execution time: {end - start:.3f} seconds")

    # Find the generation with the lowest total cost
    best_generation = min(
        range(len(generations_best_costs)),
        key=lambda i: generations_best_costs[i][0]
    )

    best_result = generations_best_costs[best_generation]

    best_cost = best_result[0]
    detailed_costs = best_result[1]
    best_chromosome = best_result[2]

    generate_report(
        best_chromosome,
        employees_data,
        tasks_data,
        best_cost,
        detailed_costs
    )

    print(
        f"Generation {best_generation}: \n"
        "------------------------------ \n"
        f"Total Cost = {best_cost}, \n"
        f"Skill Mismatch Cost = {detailed_costs[0]}, \n"
        f"Overtime Cost = {detailed_costs[1]}, \n"
        f"Imbalance Cost = {detailed_costs[2]}, \n"
        f"Proficiency Cost = {detailed_costs[3]}\n"
        "------------------------------ \n"
        f"Chromosome = {best_chromosome}"
    )



    total_costs = [cost[0] for cost in generations_best_costs]
    skill_costs = [cost[1][0] for cost in generations_best_costs]
    overtime_costs = [cost[1][1] for cost in generations_best_costs]
    imbalance_costs = [cost[1][2] for cost in generations_best_costs]
    proficiency_costs = [cost[1][3] for cost in generations_best_costs]

    plt.plot(total_costs, label="Total Cost")
    plt.plot(skill_costs, label="Skill Cost")
    plt.plot(overtime_costs, label="Overtime Cost")
    plt.plot(imbalance_costs, label="Imbalance Cost")
    plt.plot(proficiency_costs, label="Proficiency Cost")

    plt.xlabel("Generation")
    plt.ylabel("Cost")
    plt.title("Genetic Algorithm Performance")
    plt.legend()
    plt.show()

