from query import create
from splitter.split_data import splitter_main

def start_generation(repo_path: str):
    """
    This script defines the main execution flow for the documentation generation process.
    The steps include:
    1. Cloning the repository using the provided URL.
    2. Iterating through the repository to create embeddings.
    3. Utilizing the `create` function from `query.py` to generate the documentation.
    """

    # Create embeddings
    splitter_main(repo_path)
    
    # Call the create function to start generating documentation
    create()