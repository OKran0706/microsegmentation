from string import Template
import os

def create_namespace_from_template(template_file, namespace_name):
    # namespace_name=namespace_name.lower()
    # Load the template
    with open(template_file, 'r') as file:
        template_content = Template(file.read())
    
    # Substitute the placeholder with the actual namespace name
    namespace_yaml = template_content.substitute(namespace_name=namespace_name)
    
    # Define the filename for the generated YAML
    filename = f"{namespace_name}-namespace.yaml"
    
    # Save the YAML to a file
    with open('namespaces/'+filename, 'w') as file:
        file.write(namespace_yaml)
    print(f"Generated YAML for namespace '{namespace_name}' saved to {filename}")

def generate_and_save_namespaces(namespace_names):
# Example usage
    template_file_path = 'namespace_template.yaml'
    # namespace_names = ['example-namespace1', 'example-namespace2', 'example-namespace3']

    for name in namespace_names:
        create_namespace_from_template(template_file_path, name)
