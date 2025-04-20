from dotenv import load_dotenv
import os
import openai
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from system_prompt.base_prompt import system_prompt
from system_prompt.plan_prompt import generate_planning_prompt
from tools.create_tools import list_output_structure
from tools.execution_tools import create_plan_file

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

messages = [
    {"role": "system", "content": system_prompt}
]

def planning_agent():
    proj_structure = list_output_structure()

    planning_prompt = generate_planning_prompt(proj_structure)
    messages.append({ "role": "user", "content": planning_prompt })

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )

    create_plan_file(response.choices[0].message.content)