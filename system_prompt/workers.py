from agents.worker_1_planner import planner_worker
from agents.worker_2 import executor_worker

workers = {
    "planner_worker": {
        "fn": planner_worker,
        "description": "He is responsible to create the plan for the documentation process of a codebase."
    },
    "executor_worker": {
        "fn": executor_worker,
        "description": " He is responsible to execute the plan created by the planner."
    }
}