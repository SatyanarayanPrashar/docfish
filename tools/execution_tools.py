import subprocess

from termcolor import colored

def run_command(command: str, cwd: str = None, timeout: int = 10) -> dict:
    """
    Runs a shell command and prints logs in real-time.

    Args:
        command (str): The command to run.
        cwd (str, optional): Directory to run the command in.
        timeout (int, optional): Maximum duration to run the command.

    Returns:
        dict: {
            'status': 'Success' or 'Failure' or 'error',
            'message': Combined stdout and stderr output
        }
    """
    print(colored(f'Running command: {command}', 'yellow'))
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            cwd=cwd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

        output = []

        # Real-time output reading
        for line in iter(process.stdout.readline, ''):
            print(line, end='')
            output.append(line)

        process.stdout.close()
        process.wait(timeout=timeout)

        return {
            'status': 'success' if process.returncode == 0 else 'error',
            'message': ''.join(output).strip()
        }
    
    except subprocess.TimeoutExpired:
        process.kill()
        return {
            'status': 'error',
            'message': 'Command timed out'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }
    
def create_plan_file(plan: str):
    """
    Creates a plan file with the given content.

    Args:
        plan (str): The content of the plan.
    """
    if isinstance(plan, str):
        plan = plan.encode().decode('unicode_escape')

    # Create and write to the file
    with open("plan.txt", "w") as file:
        file.write(plan)
    
    print(colored(f"Plan file created.", 'green'))

def read_plan_file():
    """
    Reads the content of the plan file.

    Returns:
        str: The content of the plan file.
    """
    with open("plan.txt", "r") as file:
        plan = file.read()

    print(f"plan: {plan}")
    if not plan:
        print(colored("Plan file is empty.", 'red'))
        return "Plan is not created yet, use create_plan_file to create a plan file."

    return plan