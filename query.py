import json
from dotenv import load_dotenv
import os
import openai
from termcolor import colored
from splitter.create_database import generate_embedding
from system_prompt.tools import tools
from tools.execution_tools import run_command
from system_prompt.base_prompt import system_prompt

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

messages = [
    {"role": "system", "content": system_prompt},
]

def create(git_url: str):
    try:
        repo_name = git_url.split('/')[-1]
        output_dir = os.path.join(os.getcwd(), "clone_repos")
        code_path = os.path.join(output_dir, repo_name)

        # run_command(f"git clone {git_url} {code_path}")
    except Exception as e:
        print(f"Error cloning repository: {e}")
        return

    generate_embedding(code_path=code_path, repo_name="attendanceSystem.git")

    print(colored(f"Codebase structure generated successfully at. {code_path}", "green"))

    while True:

        messages.append({ "role": "user", "content": "The plan is already created and is saved at plan file. You can start directly at documentor_mode." })
        while True:
            response = client.chat.completions.create(
                model="gpt-4o",
                response_format={"type": "json_object"},
                messages=messages
            )

            parsed_output = json.loads(response.choices[0].message.content)
            messages.append({ "role": "assistant", "content": json.dumps(parsed_output) })

            if parsed_output.get("mode") == "planner_mode":
                print(f"🔍: {parsed_output.get("content")}")
                tool_name = parsed_output.get("function")
                tool_input = parsed_output.get("input")
                if tool_name:
                    if tools.get(tool_name, False) != False:
                        output = tools[tool_name].get("fn")(tool_input)
                        messages.append({ "role": "user", "content": json.dumps({ "mode": "planner_mode", "output":  output}) })
                        continue
                    else:
                        print(f"Tool not found: {parsed_output}")
                        break
                continue

            print("\n\n")

            if parsed_output.get("mode") == "judge_mode":
                print(f"😵‍💫: {parsed_output.get("content")}")
                tool_name = parsed_output.get("function")
                tool_input = parsed_output.get("input")
                if tool_name:
                    if tools.get(tool_name, False) != False:
                        output = tools[tool_name].get("fn")(tool_input)
                        messages.append({ "role": "user", "content": json.dumps({ "mode": "judge_mode", "output":  output}) })
                        continue
                    else:
                        print(f"Tool not found: {parsed_output}")
                        break
                continue

            print("\n\n")

            if parsed_output.get("mode") == "documentor_mode":
                print(f"📝: {parsed_output.get("content")}")
                tool_name = parsed_output.get("function")
                tool_input = parsed_output.get("input")
                if tool_name:
                    if tools.get(tool_name, False) != False:
                        output = tools[tool_name].get("fn")(tool_input)
                        messages.append({ "role": "user", "content": json.dumps({ "mode": "documentor_mode", "output":  output}) })
                        continue
                    else:
                        print(f"Tool not found: {parsed_output}")
                        break
                continue

            print("\n\n")
            
            if parsed_output.get("step") == "completed":
                print(f"🤖: We are done")
                break