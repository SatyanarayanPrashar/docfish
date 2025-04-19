from tools.create_tools import create_directory_in_output, create_file_in_directory, read_file_content
from tools.execution_tools import run_command
from tools.rag_tools import recall_code, recall_doc

tools = {
    "command_tool": {
        "fn": run_command,
        "description": "Runs a shell command and returns the result."
    },
    # "create_directory_in_output": {
    #     "fn": create_directory_in_output,
    #     "description": " Creates a directory in the output folder if it doesn't already exist."
    # },
    # "create_file_in_directory": {
    #     "fn": create_file_in_directory,
    #     "description": "Creates a file in the specified directory with the given content."
    # },
    # "read_file_content": {
    #     "fn": read_file_content,
    #     "description": "Reads the content of a file."
    # },
    "recall_code": {
        "fn": recall_code,
        "description": "Searches the codebase for specific function/feature to get more context"
    },
    "recall_doc": {
        "fn": recall_doc,
        "description": "Searches the documentation for specific feature to get more context"
    },
}


# <recall_code>: Searches the codebase for specific function/feature to get more context
# <recall_doc>: Searches the documentation for specific feature to get more context