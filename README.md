# Genetic Algorithm Task Scheduler 🧬

![Python](https://img.shields.io/badge/Python-3.12-blue)
![GitHub Tag](https://img.shields.io/github/v/tag/ahmadmrr/Genetic-Algorithm-Task-Scheduler)
![License](https://img.shields.io/github/license/ahmadmrr/Genetic-Algorithm-Task-Scheduler)
![Poetry](https://img.shields.io/badge/Dependencies-Poetry-blueviolet)

A task scheduling system that uses a Genetic Algorithm to assign tasks to employees while minimizing scheduling conflicts, workload imbalance, and skill-related penalties.

## About the Project

Assigning tasks to employees can become difficult when multiple constraints need to be considered at the same time.

For example:

- An employee may not have the required skill for a task.
- An employee may not have the required proficiency level.
- Assigning too many tasks to one employee may exceed their maximum working hours.
- The workload may be distributed unevenly between employees.

This project uses a **Genetic Algorithm (GA)** to search for good task assignments instead of checking every possible schedule.

The algorithm currently minimizes:

- Skill mismatches.
- Employee overtime.
- Workload imbalance.
- Skill proficiency differences.

The project was built from scratch in Python to better understand how Genetic Algorithms can be applied to optimization and scheduling problems.

## How It Works

Each possible schedule is represented as a **chromosome**.

Every position in the chromosome represents a task, while the value stored at that position represents the employee assigned to that task.

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

1. **Tournament Selection** - selects better schedules for reproduction.
2. **One-Point Crossover** - combines assignments from two parent schedules.
3. **Mutation** - randomly changes some employee assignments to maintain diversity.
4. **Elitism** - preserves the best schedules between generations.

## Cost Function

Each chromosome is evaluated using four cost components.

### Skill Mismatch

If an employee is assigned to a task without the required skill, a penalty is added to the schedule's cost.

```text
Skill Mismatch Cost = +10
```

Missing skills are handled separately from proficiency differences because assigning an employee without the required skill is considered a larger scheduling error.

### Proficiency Cost

Employees and tasks have proficiency levels from **1 to 10**.

If an employee has the required skill but their proficiency level differs from the task requirement, a penalty is applied.

#### Underqualification

If the employee's proficiency level is lower than the required level:

```text
Underqualification Cost =
(required level - employee level) × 0.5
```

#### Overqualification

If the employee's proficiency level is higher than the required level:

```text
Overqualification Cost =
(employee level - required level) × 0.1
```

Underqualification receives a larger penalty than overqualification.

The smaller overqualification penalty encourages the scheduler to avoid unnecessarily assigning highly skilled employees to easier tasks while still allowing such assignments when they improve the overall schedule.

### Overtime

If the total number of hours assigned to an employee exceeds their maximum working hours, a penalty is added for every overtime hour.

```text
Overtime Cost = Overtime Hours × 2
```

### Workload Imbalance

The workload of each employee is compared with the average workload across all employees.

Larger differences from the average workload result in a higher imbalance penalty.

```text
Imbalance Cost = Σ |Employee Hours - Average Hours| × 0.5
```

### Total Cost

The final chromosome cost is calculated as:

```text
Total Cost =
Skill Mismatch Cost
+ Overtime Cost
+ Workload Imbalance Cost
+ Proficiency Cost
```

The Genetic Algorithm attempts to **minimize the total cost**.

A lower cost represents a better schedule.

## Performance Optimization

Earlier versions of the project repeatedly accessed Pandas DataFrames during fitness evaluation.

Because the fitness function is executed thousands of times during a Genetic Algorithm run, repeated DataFrame access created a significant performance bottleneck.

In v2.0, employee and task data are preprocessed once before the Genetic Algorithm begins.

```text
CSV / Pandas
     ↓
Data Preprocessing
     ↓
Python Lists and Dictionaries
     ↓
Genetic Algorithm
```

The Genetic Algorithm therefore performs its repeated cost calculations using lightweight Python data structures instead of repeatedly accessing Pandas DataFrames.

Example performance improvement:

```text
Before Optimization: ~67 seconds
After Optimization:  ~1 second
```

Execution time may vary depending on hardware and Genetic Algorithm parameters.

## Project Structure

```text
Genetic-Algorithm-Task-Scheduler/
│
├── data/
│   ├── employees.csv
│   └── tasks.csv
│
├── results/
│   ├── schedule_summary.txt
│
├── src/
│   ├── data_loader.py
│   ├── chromosome.py
│   ├── fitness.py
│   ├── selection.py
│   ├── crossover.py
│   ├── mutation.py
│   ├── report.py
│   └── genetic_algorithm.py
│
├── main.py
├── pyproject.toml
├── poetry.lock
├── README.md
└── LICENSE
```

## Dataset

The project uses two CSV files.

### employees.csv

Contains employee information including:

- Employee ID.
- Employee name.
- Skills.
- Skill proficiency levels.
- Maximum working hours.

Example:

```csv
employee_id,name,skills,max_hours
0,Ahmad,"Python:9,AI:7",16
1,Sara,"Python:7,Database:9",16
```

Each employee may have multiple skills, with every skill containing a proficiency level from **1 to 10**.

### tasks.csv

Contains information about the tasks that need to be assigned.

Each task includes:

- Task ID.
- Task name.
- Required skill.
- Required proficiency level.
- Estimated working hours.

Example:

```csv
task_id,task,required_skill,required_level,hours
T01,Train classification model,AI,8,5
T02,Clean customer dataset,Python,6,3
```

The current dataset contains:

```text
20 Employees
40 Tasks
```

## Running the Project

The project uses [Poetry](https://python-poetry.org/) for dependency management.

### Clone the Repository

```bash
git clone https://github.com/ahmadmrr/Genetic-Algorithm-Task-Scheduler.git

cd Genetic-Algorithm-Task-Scheduler
```

### Install Dependencies

Make sure Poetry is installed, then run:

```bash
poetry install
```

### Run the Scheduler

```bash
poetry run python main.py
```

## Genetic Algorithm Parameters

| Parameter | Description |
| --- | --- |
| Population Size | Number of chromosomes in each generation |
| Generations | Number of generations executed |
| Mutation Rate | Probability of mutating each gene |
| Tournament Size | Number of chromosomes competing during tournament selection |
| Elite Size | Number of best chromosomes preserved unchanged |

## Generated Report

After the Genetic Algorithm finishes, the best chromosome is used to generate:

```text
results/schedule_summary.txt
```

The report contains:

- Overall cost breakdown.
- Employee workload summary.
- Number of tasks assigned to each employee.
- Remaining available hours.
- Task assignment summary.
- Required skill.
- Required proficiency level.
- Assigned employee proficiency level.

### Employee Workload Summary

Example:

```text
ID      Employee            Tasks     Workload       Max Hours   Remaining
-------------------------------------------------------------------------------------
0       Ahmad               3         14             16          2
1       Sara                2         11             16          5
2       Omar                4         16             16          0
```

### Task Assignment Summary

Example:

```text
Task ID   Task                            Employee            Skill          Req Lv    Emp Lv    Hours
--------------------------------------------------------------------------------------------------------------
T01       Train classification model      Khaled              AI             8         8         5
T02       Clean customer dataset          Ahmad               Python         6         9         3
```

This allows the complete schedule to be inspected without printing all task assignments directly to the terminal.

## Visualization

The algorithm tracks the best chromosome found in each generation.

For every generation, the following values are recorded:

- Total cost.
- Skill mismatch cost.
- Overtime cost.
- Workload imbalance cost.
- Proficiency cost.

These values are plotted across generations to show how the solution improves during the evolutionary process and how each constraint contributes to the final cost.

## Results

Because Genetic Algorithms use random selection, crossover, and mutation, different runs may produce different results even when using the same parameters.

The following result is an example of the algorithm's behavior.

### Example Run

#### Parameters

| Parameter | Value |
| --- | ---: |
| Population Size | 100 |
| Generations | 200 |
| Mutation Rate | 5% |
| Tournament Size | 5 |
| Elite Size | 2 |

#### Best Result

```text
Generation 197: 

Total Cost = 19.2, 
Skill Mismatch Cost = 0, 
Overtime Cost = 0, 
Imbalance Cost = 9.0, 
Proficiency Cost = 10.2
```

The resulting schedule contained:

- No employees assigned to tasks without the required skill.
- No employee overtime.
- A relatively balanced workload distribution.
- Remaining cost caused mainly by differences between employee proficiency levels and task requirements.

Example execution time:

```text
Execution time: 1.327 seconds
```

Execution time and final cost may vary between runs because of the stochastic nature of Genetic Algorithms.

## License

This project is licensed under the MIT License.

See the `LICENSE` file for details.