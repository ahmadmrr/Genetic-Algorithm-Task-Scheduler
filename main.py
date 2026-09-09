from src import load_data, genetic_algorithm
import matplotlib.pyplot as plt


if __name__ == "__main__":

    employees, tasks = load_data("data/employees.csv"), load_data("data/tasks.csv")

    population_size = 100
    generations = 50
    mutation_rate = 3
    tournament_size = 5
    elite_size = 2

    best_population, generations_best_costs = genetic_algorithm(
        employees.copy(), tasks.copy(), population_size, generations, mutation_rate, tournament_size, elite_size
    )


    best_generation = generations_best_costs.index(min(generations_best_costs))

    print(
    f"Generation {best_generation}: "
    f"Best Cost = {generations_best_costs[best_generation]}"
    )

    print(f"last Generation Best Cost = {generations_best_costs[-1]}")

    plt.plot(generations_best_costs)
    plt.xlabel("Generation")
    plt.ylabel("Best Cost")
    plt.title("Genetic Algorithm Performance")
    plt.show()

