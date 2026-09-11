from src import load_data, genetic_algorithm
import matplotlib.pyplot as plt


if __name__ == "__main__":

    # Load employee and task datasets
    employees = load_data("data/employees.csv")
    tasks = load_data("data/tasks.csv")

    # Genetic algorithm parameters
    population_size = 100
    generations = 100
    mutation_rate = 5
    tournament_size = 5
    elite_size = 2

    # Run the genetic algorithm
    best_population, generations_best_costs = genetic_algorithm(
        employees.copy(),
        tasks.copy(),
        population_size,
        generations,
        mutation_rate,
        tournament_size,
        elite_size
    )

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

