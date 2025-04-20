def generate_planning_prompt(proj_structure):
    plan_prompt = """
    Create the plan for the the whole documentation process. Use your knowledge of the codebase to plan it. It will include following steps:

    Project Folder structure:
        {proj_structure}

    1. Create and write Description file
        a. Read requirement or lock file to list all the dependencies
        b. If any auth is used, how it is handled
    2. Create and write Installation file
        a. Mention all the steps of setup and run the project
        b. If there is any self hosted service, mention the steps to run it
    3. License file
        a. Read the License file if it is there and mention the license details here
    4. [Feature 1]
        a. Find relevant code pieces from the codebase and understand it
        b. mention how it is implemented
    5. [Feature 2]
        a...
    6. [Feature ...]
        a...
    """

    return plan_prompt