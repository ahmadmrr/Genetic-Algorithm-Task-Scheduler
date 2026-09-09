# Genetic Algorithm Task Scheduler

A task scheduling system that uses a Genetic Algorithm to assign tasks to employees while minimizing scheduling conflicts and constraint violations.

## About the Project

Assigning tasks to employees can become difficult when multiple constraints need to be considered at the same time. For example, an employee may not have the required skill for a task, or assigning too many tasks to one employee may exceed their maximum working hours.

This project uses a **Genetic Algorithm (GA)** to search for good task assignments instead of checking every possible schedule.

In the current version, the algorithm tries to minimize:

* Skill mismatches between employees and tasks.
* Employee overtime.

The project was built from scratch in Python to better understand how Genetic Algorithms can be applied to optimization problems.

## How It Works

Each possible schedule is represented as a **chromosome**.

Every position in the chromosome represents a task, and the value stored at that position represents the employee assigned to that task.

For example:

```text
Chromosome:
[2, 0, 4, 1]

Task 0 → Employee 2
Task 1 → Employee 0
Task 2 → Employee 4
Task 3 → Employee 1
```

A population contains multiple chromosomes representing different possible schedules.

The Genetic Algorithm improves these schedules over multiple generations using:

1. **Tournament Selection** — selects better schedules for reproduction.
2. **One-Point Crossover** — combines assignments from two parent schedules.
3. **Mutation** — randomly changes some employee assignments to maintain diversity.
4. **Elitism** — preserves the best schedules between generations.

## Cost Function

Each chromosome is evaluated using a cost function.

The current version considers two constraints:

### Skill Mismatch

If an employee is assigned to a task without the required skill, a penalty is added to the schedule's cost.

```text
Skill mismatch = +10 cost
```

### Overtime

If the total hours assigned to an employee exceed their maximum working hours, a penalty is added for each overtime hour.

```text
Overtime cost = overtime hours × penalty
```

The Genetic Algorithm attempts to **minimize the total cost**.

```text
Total Cost = Skill Mismatch Cost + Overtime Cost
```

A lower cost represents a better schedule, and a cost of `0` means that all current constraints have been satisfied.

## Project Structure

```text
genetic-scheduler/
├── data/
│   ├── employees.csv
│   └── tasks.csv
│
├── src/
│   ├── data_loader.py
│   ├── chromosome.py
│   ├── fitness.py
│   ├── selection.py
│   ├── crossover.py
│   ├── mutation.py
│   └── genetic_algorithm.py
│
├── main.py
├── requirements.txt
└── README.md
```

## Dataset

The dataset is divided into two CSV files:

* `employees.csv`: Contains information about the employees, including their ID, name, skills, and maximum working hours.

* `tasks.csv`: Contains the tasks that need to be assigned, including the task ID, task name, required skill, and estimated working hours.


## Running the Project

```bash
pip install -r requirements.txt
python main.py
```

## Genetic Algorithm Parameters

| Parameter       | Description                                             |
| --------------- | ------------------------------------------------------- |
| Population Size | Number of chromosomes in each generation                |
| Generations     | Number of generations                                   |
| Mutation Rate   | Probability of mutating each gene                       |
| Tournament Size | Number of chromosomes competing in tournament selection |
| Elite Size      | Number of best chromosomes preserved unchanged          |

## Results


The algorithm was tested multiple times with different Genetic Algorithm parameters. Each experiment was executed 10 times because the algorithm contains random operations and may produce different results between runs.

### Experiment 1

**Parameters:**

| Parameter       | Value |
| --------------- | ----: |
| Population Size |   100 |
| Generations     |    50 |
| Mutation Rate   |    5% |
| Tournament Size |     3 |
| Elite Size      |     2 |

**Results:**

* Best cost: **0**
* Worst cost: **4**
* Average final cost: **1.6**
* Successful runs reaching cost 0: **3/10**

### Experiment 2

**Parameters:**

| Parameter       | Value |
| --------------- | ----: |
| Population Size |   100 |
| Generations     |    50 |
| Mutation Rate   |    3% |
| Tournament Size |     5 |
| Elite Size      |     2 |

**Results:**

* Best cost: **0**
* Worst cost: **6**
* Average final cost: **1.0**
* Successful runs reaching cost 0: **7/10**

### Experiment Comparison

Experiment 2 produced better results overall. It reached a cost of `0` in 7 out of 10 runs, compared with 3 out of 10 runs in Experiment 1. It also achieved a lower average final cost of `1.0`.

However, Experiment 1 had a lower worst-case cost of `4`, compared with `6` in Experiment 2.


## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
