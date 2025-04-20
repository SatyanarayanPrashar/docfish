import json
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
import os
import openai
from langchain_qdrant import QdrantVectorStore
from splitter.create_database import generate_embedding
from splitter.split_data import splitter_main
from system_prompt.tools import tools
from tools.execution_tools import run_command

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

# Load the system prompt from the system_prompt.txt file
with open("system_prompt/system_prompt.txt", "r") as file:
    system_prompt = file.read()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

messages = [
    {"role": "system", "content": system_prompt},
]

def create(git_url: str):
    try:
        run_command(f"git clone {git_url}")
    except Exception as e:
        print(f"Error cloning repository: {e}")
        return

    repo_name = git_url.split('/')[-1]
    if repo_name.endswith('.git'):
        repo_name = repo_name[:-4]
    cloned_repo_path = f"./{repo_name}"
    generate_embedding(code_path=cloned_repo_path)

    while True:
        messages.append({ "role": "user", "content": "Analyse my codebase structure and learn how the features are implemented. Then create me a detailed documentation for it." })

        while True:
            response = client.chat.completions.create(
                model="gpt-4o",
                response_format={"type": "json_object"},
                messages=messages
            )

            parsed_output = json.loads(response.choices[0].message.content)
            messages.append({ "role": "assistant", "content": json.dumps(parsed_output) })

            if parsed_output.get("stage") == "Analysis":
                print(f"🔍: {parsed_output.get("content")}")
                continue

            if parsed_output.get("stage") == "Planning":
                print(f"🧠: {parsed_output.get("content")}")
                continue
            
            if parsed_output.get("stage") == "Executing":
                tool_name = parsed_output.get("function")
                tool_input = parsed_output.get("input")

                if tools.get(tool_name, False) != False:
                    output = tools[tool_name].get("fn")(tool_input)
                    messages.append({ "role": "user", "content": json.dumps({ "stage": "Executing", "output":  output}) })
                    continue
                else:
                    print(f"Tool not found: {parsed_output}")
                    break
            
            if parsed_output.get("step") == "output":
                print(f"🤖: {parsed_output.get("content")}")
                break