import subprocess


def get_system_username():
    # Run the 'whoami' command
    result = subprocess.run(['whoami'], stdout=subprocess.PIPE, text=True)
    return result.stdout.strip()