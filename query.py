import json
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
import os
import openai
from langchain_qdrant import QdrantVectorStore
from tools.execution_tools import run_command
from tools.rag_tools import recall_code, recall_doc

tools = {
    "command_tool": {
        "fn": run_command,
        "description": "Runs a shell command and returns the result."
    },
    "recall_code": {
        "fn": recall_code,
        "description": "Searches the codebase for specific function/feature to get more context"
    },
    "recall_doc": {
        "fn": recall_doc,
        "description": "Searches the documentation for specific feature to get more context"
    },
}

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

# Create embeddings for the split documents
embedder = OpenAIEmbeddings(
    model="text-embedding-3-large",
    api_key=api_key
)

retriever = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="code_repo_embeddings",
    embedding=embedder
)

# Load the system prompt from the system_prompt.txt file
with open("system_prompt/system_prompt.txt", "r") as file:
    system_prompt = file.read()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

messages = [
    {"role": "system", "content": system_prompt},
]

while True:
    user_query = input('>> ')
    messages.append({ "role": "user", "content": user_query })

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