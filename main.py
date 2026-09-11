from src import load_data, genetic_algorithm
import matplotlib.pyplot as plt
from time import perf_counter

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

        employees_data.append(data)


    tasks_data = []

    for task_id in range(tasks.shape[0]):
        data = {
            "required_skill": tasks.loc[task_id, "required_skill"],
            "required_level": int(tasks.loc[task_id, "required_level"]),
            "hours": int(tasks.loc[task_id, "hours"])
        }

        tasks_data.append(data)


    # Genetic algorithm parameters
    population_size = 100
    generations = 200
    mutation_rate = 5
    tournament_size = 3
    elite_size = 2

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

    best_cost = generations_best_costs[best_generation]
    last_cost = generations_best_costs[-1]

    print(
        f"Generation {best_generation}: \n"
        f"Total Cost = {best_cost[0]}, \n"
        f"Skill Cost = {best_cost[1][0]}, \n"
        f"Overtime Cost = {best_cost[1][1]}, \n"
        f"Imbalance Cost = {best_cost[1][2]}\n"
    )

    print('======================================')

    print(
        f"Last Generation: \n"
        f"Total Cost = {last_cost[0]}, \n"
        f"Skill Cost = {last_cost[1][0]}, \n"
        f"Overtime Cost = {last_cost[1][1]}, \n"
        f"Imbalance Cost = {last_cost[1][2]}\n"
    )

    total_costs = [cost[0] for cost in generations_best_costs]
    skill_costs = [cost[1][0] for cost in generations_best_costs]
    overtime_costs = [cost[1][1] for cost in generations_best_costs]
    imbalance_costs = [cost[1][2] for cost in generations_best_costs]

    plt.plot(total_costs, label="Total Cost")
    plt.plot(skill_costs, label="Skill Cost")
    plt.plot(overtime_costs, label="Overtime Cost")
    plt.plot(imbalance_costs, label="Imbalance Cost")

    plt.xlabel("Generation")
    plt.ylabel("Cost")
    plt.title("Genetic Algorithm Performance")
    plt.legend()
    plt.show()

