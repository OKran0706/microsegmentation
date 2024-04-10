import subprocess
import os

def deploy_pod_yaml(directory,pod_names,namespace):
    print("In")
    # Ensure the directory exists
    if not os.path.exists(directory):
        print(f"The directory {directory} does not exist.")
        return -1
    flag=0
    # Iterate over all files in the specified directory
    for filename in os.listdir(directory):
        print(filename,pod_names,filename.split('-')[1] ,namespace)
        if filename.endswith(".yaml") or filename.endswith(".yml"):
            filename_1,_=filename.split('.yaml')
            if filename_1.split('-')[1] not in pod_names or filename_1.split('-')[0]!=namespace:
                print(filename,"skipped")
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
            print(f"Skipping {filename}, not a YAML file.")
        
    return flag
    
if __name__=='__main__':
    # Specify the directory containing the YAML files
    yaml_directory = 'output_pods'

    # Deploy the pods
    deploy_pod_yaml(yaml_directory)
