import os

from termcolor import colored

def create_directory_in_output(directory_name: str):
    """
    Creates a directory in the output folder if it doesn't already exist.

    Args:
        directory_name (str): The name of the directory to create.
    """
    # Get the current working directory
    current_directory = os.getcwd()
    
    # Define the output directory path
    output_directory = os.path.join(current_directory, "output", directory_name)
    
    # Create the directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        print(f"Directory '{directory_name}' created in 'output' folder.")
    else:
        print(f"Directory '{directory_name}' already exists in 'output' folder.")
    return {"status": "success", "message": f"Directory '{directory_name}' created in 'output' folder."}


def create_file_in_directory(directory_path: str, file_name: str, content: str):
    """
    Creates a file in the specified directory with the given content.

    Args:
        directory_path (str): The path to the directory where the file will be created.
        file_name (str): The name of the file to create.
        content (str): The content to write to the file.
    """
    
     # Get the current working directory
    current_directory = os.getcwd()

    # Check if 'output' is already in the directory_path
    if "output" in os.path.normpath(directory_path).split(os.sep):
        output_directory = os.path.join(current_directory, directory_path)
    else:
        output_directory = os.path.join(current_directory, "output", directory_path)

    # Make sure the directory exists
    os.makedirs(output_directory, exist_ok=True)
    
    # Define the full path for the new file
    file_path = os.path.join(output_directory, file_name)
    
     # Clean up content
    if isinstance(content, str):
        content = content.encode().decode('unicode_escape')  # convert \\n to \n
    
    # Create and write to the file
    with open(file_path, "w") as file:
        file.write(content)
    
    print(f"File '{file_name}' created in '{directory_path}'.")
    return {"status": "success", "message": f"File '{file_name}' created in '{directory_path}'."}

def generate_tree(directory, prefix=""):
    """
    Recursively generate a tree structure string for a given directory.
    """
    tree = ""
    entries = sorted(os.listdir(directory))
    for index, entry in enumerate(entries):
        entry_path = os.path.join(directory, entry)
        connector = "└── " if index == len(entries) - 1 else "├── "
        tree += prefix + connector + entry + "\n"
        if os.path.isdir(entry_path):
            extension = "    " if index == len(entries) - 1 else "│   "
            tree += generate_tree(entry_path, prefix + extension)
    return tree

def list_output_structure(dummy: str = None):
    """
    Lists the structure of the output folder in a tree format.

    Returns:
        dict: A dictionary containing the structure of the output folder.
    """
    print(colored(f"Listing the structure of the output folder... {dummy}", "green"))
    current_directory = os.getcwd()
    output_directory = os.path.join(current_directory, "clone_repos")

    if not os.path.exists(output_directory):
        return {"status": "error", "message": "Output directory does not exist."}

    tree_structure = generate_tree(output_directory)

    return {
        "status": "success",
        "message": f"Output folder structure:\n{tree_structure}"
    }

def read_file_content(file_path: str):
    """
    Reads the content of a file.
    
    Args:
        file_path (str): The path to the file to read.
        
    Returns:
        str: The content of the file.
    """
    path = "/Users/satya/Desktop/pythonProjects/docfish/clone_repos/attendanceSystem.git/" + file_path
    with open(path, "r") as file:
        content = file.read()
    
    # Return the list of directories
    return {"status": "success", "message": content}
    