import subprocess
import yaml
from string import Template
import os
from kubernetes import client, config
def default_deny(namespaces):
    def create_policy_from_template(template_file, namespace_name):
        # Load the template
        with open(template_file, 'r') as file:
            template_content = Template(file.read())
        
        # Substitute the placeholder with the actual namespace name
        namespace_yaml = template_content.substitute(namespace_name=namespace_name)
        
        # Define the filename for the generated YAML
        filename = f"{namespace_name}-default-deny.yaml"
        
        # Ensure the output directory exists
        output_dir = 'policies'
        os.makedirs(output_dir, exist_ok=True)

        file_path = os.path.join(output_dir, filename)
        
        # Save the YAML to a file in the specified directory
        with open(file_path, 'w') as file:
            file.write(namespace_yaml)
        print(f"Generated YAML for namespace '{namespace_name}' default deny policy saved to {os.path.join(output_dir, filename)}")

        try:
            # Using subprocess to run kubectl apply
            subprocess.run(["kubectl", "apply", "-f", file_path], check=True)
            print(f"Successfully deployed: {file_path}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to deploy {file_path}: {e}")
            
    def generate_save_deploy(namespace_names):
        template_file_path = 'default_deny_template.yaml'

        for name in namespace_names:
            create_policy_from_template(template_file_path, name)
        
    generate_save_deploy(namespaces)

def add_connection_and_apply(namespace_from, namespace_to):
    # Load the template from the file
    with open('connect_namespaces_template.yaml', 'r') as file:
        network_policy_template = Template(file.read())
    
    # Use the substitute method of Template to replace placeholders with actual namespace names
    network_policy_yaml = network_policy_template.substitute(from_ns=namespace_from, to_ns=namespace_to)
    
    # Writing the generated YAML to a temporary file
    tmp_file_path = f"policies/{namespace_from}_{namespace_to}-connect-policy.yaml"
    with open(tmp_file_path, "w") as tmp_file:
        tmp_file.write(network_policy_yaml)
    
    # Applying the network policy using kubectl
    try:
        subprocess.run(["kubectl", "apply", "-f", tmp_file_path], check=True)
        print(f"NetworkPolicy applied successfully for namespace {namespace_from} to {namespace_to}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to apply NetworkPolicy: {e}")

def delete_connection_policy(namespace1, namespace2):
    # Load Kubernetes configuration, e.g., from ~/.kube/config
    config.load_kube_config()

    # Define the name of the NetworkPolicy you want to delete
    network_policy_name = f"allow-from-{namespace1}-to-{namespace2}"

    # Create an instance of the API class
    k8s_networking_api = client.NetworkingV1Api()

    try:
        # Delete the NetworkPolicy
        api_response = k8s_networking_api.delete_namespaced_network_policy(
            name=network_policy_name,
            namespace=namespace2,
            body=client.V1DeleteOptions(),
        )
        print(f"NetworkPolicy '{network_policy_name}' deleted. Status='{api_response.status}'")
    except client.exceptions.ApiException as e:
        if e.status == 404:
            print(f"NetworkPolicy '{network_policy_name}' not found in namespace '{namespace2}'.")
        else:
            print(f"Failed to delete NetworkPolicy '{network_policy_name}': {e}")
    network_policy_name = f"allow-from-{namespace1}-to-{namespace2}"

    # Now reversed
    network_policy_name = f"allow-from-{namespace2}-to-{namespace1}"


    try:
        # Delete the NetworkPolicy
        api_response = k8s_networking_api.delete_namespaced_network_policy(
            name=network_policy_name,
            namespace=namespace1,
            body=client.V1DeleteOptions(),
        )
        print(f"NetworkPolicy '{network_policy_name}' deleted. Status='{api_response.status}'")
    except client.exceptions.ApiException as e:
        if e.status == 404:
            print(f"NetworkPolicy '{network_policy_name}' not found in namespace '{namespace1}'.")
        else:
            print(f"Failed to delete NetworkPolicy '{network_policy_name}': {e}")


      
def add_connection_to_necessary_namespaces(namespace,necessary=['default','kube-system','kube-node-lease','kube-public']):
    # Load the template from the file
    with open('connect_necessary_ns.yaml', 'r') as file:
        network_policy_template = Template(file.read())
    
    # Use the substitute method of Template to replace placeholders with actual namespace names
    for necessary_ns in necessary:

        network_policy_yaml = network_policy_template.substitute(from_ns=necessary_ns, to_ns=namespace)
        
        # Writing the generated YAML to a temporary file
        tmp_file_path = f"policies/necessary_{namespace}_{necessary_ns}-connect-policy.yaml"
        with open(tmp_file_path, "w") as tmp_file:
            tmp_file.write(network_policy_yaml)
        
        # Applying the network policy using kubectl
        try:
            subprocess.run(["kubectl", "apply", "-f", tmp_file_path], check=True)
            print(f"NetworkPolicy applied successfully for namespace {necessary_ns} to {namespace}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to apply NetworkPolicy: {e}")      
        



# def add_connection(namespace_from,namespace_to):

