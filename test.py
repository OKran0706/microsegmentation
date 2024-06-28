import os
import subprocess

# Print the current working directory
print("Current Working Directory:", os.getcwd())

script_path = 'vcluster-ssh.sh'

try:
    # If the script is not being found, you can explicitly set the path
    full_path = os.path.join(os.getcwd(), script_path)

    # Check if the script exists at the expected location
    if not os.path.exists(full_path):
        print(f"Script not found at {full_path}")
    else:
        # Execute the shell script
        result = subprocess.run([full_path], capture_output=True, text=True, check=True)
        print("Shell script ran successfully.")
        print("Output:", result.stdout)
except subprocess.CalledProcessError as e:
    print("Failed to run shell script.")
    print("Error:", e.stderr)
except FileNotFoundError:
    print(f"Script file {script_path} not found.")
