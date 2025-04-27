from agents.worker_docsfish import worker_docsfish
from agents.worker_planner import planner_worker
from agents.worker_executer import executor_worker

workers = {
    "docsfish": {
        "fn": worker_docsfish,
        "description": "He is responsible to worker_docsfish the plan for the documentation process of a codebase."
    },
    "planner_worker": {
        "fn": planner_worker,
        "description": "He is responsible to worker_docsfish the plan for the documentation process of a codebase."
    },
    "executor_worker": {
        "fn": executor_worker,
        "description": " He is responsible to execute the plan created by the planner."
    },
}