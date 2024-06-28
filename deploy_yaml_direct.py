import subprocess

def create_resources_from_yaml(yaml_file):
    """
    Create Kubernetes resources from a YAML file using kubectl.
    
    Args:
    yaml_file (str): Path to the YAML file that contains Kubernetes resource definitions.
    """
    try:
        # Execute the kubectl command to apply the YAML file
        result = subprocess.run(["kubectl", "apply", "-f", yaml_file], check=True, capture_output=True, text=True)
        print("Resources created successfully:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Failed to create resources:")
        print(e.stderr)

