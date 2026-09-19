import pandas as pd

from src.preprocessing import (
    preprocess_employees,
    preprocess_tasks,
)


def test_preprocess_employees():
    employees = pd.DataFrame(
        {
            "name": ["Bob"],
            "skills": ["Python:4, SQL:3"],
            "available_hours": [40],
        }
    )

    result = preprocess_employees(employees)

    assert result == [
        {
            "Python": 4,
            "SQL": 3,
            "available_hours": 40,
            "name": "Bob",
        }
    ]


def test_preprocess_tasks():
    tasks = pd.DataFrame(
        {
            "task_id": [1],
            "task": ["Build API"],
            "required_skills": ["Python:4, SQL:2"],
            "hours": [8],
            "priority": [3],
        }
    )

    result = preprocess_tasks(tasks)

    assert result == [
        {
            "task_id": 1,
            "task": "Build API",
            "required_skills": {
                "Python": 4,
                "SQL": 2,
            },
            "hours": 8,
            "priority": 3,
        }
    ]
