import psutil

def is_process_running(name):
    """
    Checks if a process with the given name is currently running on the system.

    Args:
        name (str): The name of the process to look for (e.g., 'LeagueClient.exe').

    Returns:
        bool: True if a process with the specified name is running, False otherwise.
    """
    # Iterate through all running processes and retrieve their 'name' attribute
    for proc in psutil.process_iter(['name']):
        # Compare the process name to the provided name
        if proc.info['name'] == name:
            return True  # Process is found
    return False  # Process was not found