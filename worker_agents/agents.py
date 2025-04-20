from worker_agents.planning_agent.main import planning_agent

agents = {
    "planning_worker": {
        "fn": planning_agent(),
        "description": "This worker is responsible for creating a plan for documentation process."
    }
}