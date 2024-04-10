import subprocess
import os

def deploy_namespace_yaml(directory,res):
    # Ensure the directory exists
    if not os.path.exists(directory):
        print(f"The directory {directory} does not exist.")
        return 1
    flag=0
    
    # Filter for namespace YAML files to avoid deploying unintended resources
    for filename in os.listdir(directory):
        if (filename.endswith(".yaml") or filename.endswith(".yml")) and "namespace" in filename :
            if filename.split('-')[0] not in res:
                continue
            # Construct the full file path
            filepath = os.path.join(directory, filename)
            
            # Deploy the YAML file using kubectl
            try:
                print(f"Deploying {filename}...")
                subprocess.run(["kubectl", "apply", "-f", filepath], check=True)
                print(f"Successfully deployed {filename}.")
            except subprocess.CalledProcessError as e:
                print(f"Failed to deploy {filename}: {e}")
                flag=1
            except Exception as e:
                print(f"An error occurred: {e}")
                flag=1
        else:
            print(f"Skipping {filename}, not a namespace YAML file.")
    return flag

# # Specify the directory containing the YAML files
# yaml_directory = 'namespaces'  # Update this path to the directory where your namespace YAML files are stored

# # Deploy the namespaces
# deploy_namespace_yaml(yaml_directory)
