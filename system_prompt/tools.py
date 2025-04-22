from tools.execution_tools import create_plan_file, read_plan_file, run_command
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
    "recall_doc": {
        "fn": read_plan_file,
        "description": "Reads the content of the plan file."
    },
    "create_plan_file": {
        "fn": create_plan_file,
        "description": "Creates a plan file with the given content."
    },
}