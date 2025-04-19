from tools.create_tools import create_directory_in_output, create_file_in_directory, read_file_content
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