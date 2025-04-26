from termcolor import colored
import json
from agents.base_llm import base_llm_call
from system_prompt.tools import tools
from system_prompt.worker_1_prompt import planner_prompt

def planner_worker(message: str) -> str:
    messages = [
        {"role": "system", "content": planner_prompt},
    ]
    messages.append({ "role": "user", "content": message })

    while True:
        try:
            while True:
                response = base_llm_call(messages)

                parsed_output = json.loads(response)
                messages.append({ "role": "assistant", "content": json.dumps(parsed_output) })

                print(f"📝: {parsed_output.get('content')}")

                if parsed_output.get("function"):
                    tool_name = parsed_output.get("function")
                    tool_input = parsed_output.get("input")

                    if tool_name:
                        if tools.get(tool_name):
                            output = tools[tool_name].get("fn")(tool_input)
                            messages.append({
                                "role": "assistant",
                                "content": json.dumps({
                                    "agent": "planner_worker",
                                    "output": output
                                })
                            })

                            if output == "Plan created successfully.":
                                print(colored("✅ Plan created. Exiting...", "green"))
                                break
                            continue

                    continue
            break

        except Exception as e:
            print(colored(f"Error: {e}", "red"))
            break
    return "Plan is created successfully. You can move to execution"
   