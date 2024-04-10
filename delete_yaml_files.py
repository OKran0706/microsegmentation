import os
import glob
def delete_all_yaml_files(directory):
    # Create a pattern to match all .yaml files
    pattern = os.path.join(directory, '*.yaml')
    
    # Use glob to find all files in the directory matching the pattern
    yaml_files = glob.glob(pattern)
    
    # Loop through the list of files and delete each one
    for file_path in yaml_files:
        try:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        except OSError as e:
            print(f"Error deleting {file_path}: {e}")