from termcolor import colored
import json
from dotenv import load_dotenv
import os
import openai
from system_prompt.tools import tools
from system_prompt.worker_1_prompt import planner_prompt

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def planner_worker(message: str) -> str:
    print(colored(f"Processing message: {message}", "green"))
    return "Plan is created successfully. You can move to execution"
   