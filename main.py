from agents.worker_docsfish import worker_docsfish
from splitter.split_data import splitter_main

def start_generation(repo_path: str):
    """
    This script defines the main execution flow for the documentation generation process.
    The steps include:
    1. Cloning the repository using the provided URL.
    2. Iterating through the repository to worker_docsfish embeddings.
    3. Utilizing the `worker_docsfish` function from `query.py` to generate the documentation.
    """

    # Create embeddings
    splitter_main(repo_path)
    
    # Call the worker_docsfish function to start generating documentation
    worker_docsfish()