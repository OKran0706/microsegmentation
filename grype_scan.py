import subprocess
import json
import re

def is_valid_image_name(image_name):
    regex = "^[a-zA-Z\d_]:?[a-zA-Z\d_.]$"
    if re.match(regex, image_name):
        return True
    else:
        return False

def scan_image_with_grype(image_name):
    """
    Scans the specified container image using Grype and returns the vulnerability scan results.
    
    Args:
        image_name (str): The name of the container image to scan.
        
    Returns:
        dict: The parsed JSON vulnerability report.
    """
    # if not is_valid_image_name(image_name):
    #     print("Invalid Image Name")
    #     return 
    try:

        script = f'echo "Press any key to exit"; read -n 1'

            # Launch the command in a new GNOME Terminal window
        subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', f'grype {image_name}; {script}'])

    except subprocess.SubprocessError as e:
        print(f"Failed to execute command: {e}")

# Example usage
if __name__=="__main__":
    image_to_scan = "ubuntu:latest"
    scan_image_with_grype(image_to_scan)


