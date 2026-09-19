from src.fitness import (
    imbalance_cost,
    overtime_cost,
    priority_cost,
    proficiency_cost,
    skill_mismatch_cost,
)


def test_skill_mismatch_cost():
    employees_data = [
        {
            "Python": 4,
            "SQL": 3,
            "available_hours": 40,
            "name": "Employee 0",
        },
        {
            "Java": 4,
            "available_hours": 40,
            "name": "Employee 1",
        },
    ]

    tasks_data = [
        {
            "required_skills": {
                "Python": 3,
                "SQL": 2,
            },
            "hours": 5,
            "priority": 2,
        },
        {
            "required_skills": {
                "Java": 3,
            },
            "hours": 4,
            "priority": 2,
        },
    ]

    chromosome = [0, 0]

    result = skill_mismatch_cost(
        chromosome,
        employees_data,
        tasks_data,
    )

    assert result == 50

    valid_chromosome = [0, 1]

    result = skill_mismatch_cost(
        valid_chromosome,
        employees_data,
        tasks_data,
    )

    assert result == 0


def test_overtime_cost():
    employees_data = [
        {
            "name": "Employee 1",
            "available_hours": 10,
        }
    ]

    tasks_data = [
        {
            "hours": 6,
        },
        {
            "hours": 7,
        },
    ]

    chromosome = [0, 0]

    result = overtime_cost(
        chromosome,
        employees_data,
        tasks_data,
    )

    assert result == 15

    chromosome = [0]

    result = overtime_cost(
        chromosome,
        employees_data,
        tasks_data,
    )

    assert result == 0


def test_proficiency_cost():
    employees_data = [
        {
            "Python": 2,
            "name": "Employee 0",
            "available_hours": 40,
        },
        {
            "Python": 4,
            "name": "Employee 1",
            "available_hours": 40,
        },
    ]

    tasks_data = [
        {
            "required_skills": {"Python": 4},
            "hours": 5,
            "priority": 2,
        }
    ]

    assert (
        proficiency_cost(
            [0],
            employees_data,
            tasks_data,
        )
        == 1
    )

    assert (
        proficiency_cost(
            [1],
            employees_data,
            tasks_data,
        )
        == 0
    )


def test_imbalance_cost():
    tasks_data = [
        {"hours": 10},
        {"hours": 10},
    ]

    assert (
        imbalance_cost(
            [0, 0],
            tasks_data,
            2,
        )
        == 10
    )

    assert (
        imbalance_cost(
            [0, 1],
            tasks_data,
            2,
        )
        == 0
    )


def test_priority_cost():
    tasks_data = [
        {
            "hours": 10,
            "priority": 4,
        },
        {
            "hours": 10,
            "priority": 4,
        },
    ]

    assert (
        priority_cost(
            [0, 0],
            tasks_data,
            2,
        )
        == 24
    )

    assert (
        priority_cost(
            [0, 1],
            tasks_data,
            2,
        )
        == 0
    )
