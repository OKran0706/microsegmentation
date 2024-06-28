import subprocess

def kubectl_copy(source_file, pod_name, namespace='default'):
    """
    Copy a file into a pod using kubectl cp.

    Args:
    source_file (str): The path to the source file on the local filesystem.
    pod_name (str): The name of the pod where the file should be copied.
    namespace (str): The Kubernetes namespace of the pod. Defaults to 'default'.
    """
    # Command to copy the file into the specified pod
    destination = f"{pod_name}:/{source_file}"
    if namespace:
        destination = f"{namespace}/{destination}"

    command = ["kubectl", "cp", source_file, destination]

    # Run the subprocess command
    try:
        subprocess.run(command, check=True)
        print("File copied successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

