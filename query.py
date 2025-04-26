import json
from termcolor import colored
from agents.base_llm import base_llm_call
from splitter.create_database import generate_embedding
from system_prompt.workers import workers
from system_prompt.tools import tools
from tools.execution_tools import run_command
from system_prompt.base_prompt import system_prompt
from tools.generate_streamlit_pages import generate_pages

def create(git_url: str):
    # try:
    #     repo_name = git_url.split('/')[-1]
    #     output_dir = os.path.join(os.getcwd(), "clone_repos")
    #     code_path = os.path.join(output_dir, repo_name)

    #     run_command(f"git clone {git_url} {code_path}")
    # except Exception as e:
    #     print(f"Error cloning repository: {e}")
    #     return

    # generate_embedding(code_path=code_path, repo_name="attendanceSystem.git")

    messages = [
        {"role": "system", "content": system_prompt},
    ]
    messages.append({ "role": "user", "content": "Create me the documentation for this codebase." })

    while True:
        try:
            while True:
                response = base_llm_call(messages)

                parsed_output = json.loads(response)
                messages.append({ "role": "assistant", "content": json.dumps(parsed_output) })

                print(f"🤖: {parsed_output.get('content')}")

                if parsed_output.get("function"):
                    tool_name = parsed_output.get("function")
                    tool_input = parsed_output.get("input")

                    if tool_name:
                        if tools.get(tool_name):
                            output = tools[tool_name].get("fn")(tool_input)
                            messages.append({
                                "role": "assistant",
                                "content": json.dumps({
                                    "agent": "Docsfish",
                                    "output": output
                                })
                            })
                            
                            # 🔥 check if documentation is done
                            if output == "Documentation is created successfully.":
                                print(colored("✅ Documentation created. Exiting...", "green"))
                                break
                            continue

                        if workers.get(tool_name):
                            output = workers[tool_name].get("fn")(tool_input)
                            print(f"planner output: {output}")
                            messages.append({
                                "role": "assistant",
                                "content": json.dumps({
                                    "agent": tool_name,
                                    "output": output
                                })
                            })
                            
                            # 🔥 check if documentation is done
                            if output == "Documentation is created successfully.":
                                print(colored("✅ Documentation created. Exiting...", "green"))
                                break
                            continue
                    continue
            break

        except Exception as e:
            print(colored(f"Error: {e}", "red"))
            break