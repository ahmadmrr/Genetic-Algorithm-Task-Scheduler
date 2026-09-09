from src import load_data, genetic_algorithm
import matplotlib.pyplot as plt


if __name__ == "__main__":

    # Load employee and task datasets
    employees = load_data("data/employees.csv")
    tasks = load_data("data/tasks.csv")

    # Genetic algorithm parameters
    population_size = 100
    generations = 50
    mutation_rate = 3
    tournament_size = 5
    elite_size = 2

    # Run the genetic algorithm
    best_population, generations_best_costs = genetic_algorithm(
        employees.copy(), tasks.copy(), population_size, generations, mutation_rate, tournament_size, elite_size
    )

    # Find the generation with the lowest cost
    best_generation = generations_best_costs.index(min(generations_best_costs))

    print(
    f"Generation {best_generation}: "
    f"Best Cost = {generations_best_costs[best_generation]}"
    )

    print(f"last Generation Best Cost = {generations_best_costs[-1]}")

    # Plot the best cost across generations
    plt.plot(generations_best_costs)
    plt.xlabel("Generation")
    plt.ylabel("Best Cost")
    plt.title("Genetic Algorithm Performance")
    plt.show()

