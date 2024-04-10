from string import Template
from datetime import datetime
import os

# Function to load pod template from a file
def load_template(file_path):
    with open(file_path, 'r') as file:
        template_content = file.read()
    return Template(template_content)

# Function to generate pod YAML with specific parameters and save to a file
def generate_and_save_pod_yaml(template, pod_name, namespace):
    # Generate a timestamp for label uniqueness
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    
    # Substitute placeholders in the template, including the unique label
    pod_yaml = template.substitute(pod_name=pod_name, namespace=namespace, timestamp=timestamp)
    
    # Define the filename using the pod name and namespace
    filename = f"{namespace}-{pod_name}.yaml"
    
    # Create directory if it doesn't exist
    output_dir = 'output_pods'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Write the pod YAML to a file in the specified directory
    with open(os.path.join(output_dir, filename), 'w') as file:
        file.write(pod_yaml)
    print(f"Saved: {filename}")

def generate_and_save_pods(pod_names,namespace):
	template_file_path = 'pod_template.yaml'

	# Load the template
	template = load_template(template_file_path)

	# Example usage
	#pod_names = ['busybox-pod1', 'busybox-pod2', 'busybox-pod3']
	#namespace_names = ['example-namespace1', 'example-namespace2', 'example-namespace3']

	for pod_name in pod_names:
	    generate_and_save_pod_yaml(template, pod_name, namespace)

