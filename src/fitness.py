
def skill_mismatch_cost(chromosome, employees, tasks):
    cost = 0
    for i, j in enumerate(chromosome):
        if tasks.loc[i, 'required_skill'] in employees.loc[j, 'skills']:
            continue
        else:
            cost += 10
    return cost


def overtime_cost(chromosome, employees, tasks):
    cost = 0
    hours_map = {}
    for i, j in enumerate(chromosome):
        if j not in hours_map.keys():
            hours_map[j] = tasks.loc[i, 'hours']
        else:
            hours_map[j] += tasks.loc[i, 'hours']

    for key, value in hours_map.items():
        if value > employees.loc[key, 'max_hours']:
            cost += (value - employees.loc[key, 'max_hours']) * 2
    return cost


def cost(population, employees, tasks):
    costs = []

    for chromosome in population:

        skill_cost = skill_mismatch_cost(chromosome, employees.copy(), tasks.copy())
        overtime = overtime_cost(chromosome, employees.copy(), tasks.copy())
        costs.append(skill_cost + overtime)
    
    return costs

