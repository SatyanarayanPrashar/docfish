import json
from dotenv import load_dotenv
import os
import openai
from termcolor import colored
from splitter.create_database import generate_embedding
from system_prompt.tools import tools
from tools.execution_tools import run_command
from system_prompt.base_prompt import system_prompt
import streamlit as st

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

messages = [
    {"role": "system", "content": "You are a software  engineer help the user to understand how the features are implemented in his codebase."},
]

query = st.text_input("Ask your question", key="query_input")

if st.button("Submit") or query:
    if query:
        messages.append({"role": "user", "content": query})
        response = process(query)
        st.write(response)


def process(query: str):
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=messages
    )

    parsed_output = json.loads(response.choices[0].message.content)

