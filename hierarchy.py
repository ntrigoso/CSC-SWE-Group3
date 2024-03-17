import os

def contains_target_files(directory, extensions):
    """
    Check if a directory contains files with the given extensions
    """
    for item in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, item)):
            # Recursively check in subdirectories
            if contains_target_files(os.path.join(directory, item), extensions):
                return True
        elif any(item.endswith(ext) for ext in extensions):
            return True
    return False

def print_directory_hierarchy(path, indent=0, extensions=('.py', '.html')):
    # Check if the path is a directory
    if os.path.isdir(path):
        # Only proceed if the directory contains target files
        if contains_target_files(path, extensions):
            # Print the directory name with a trailing slash
            print('    ' * indent + os.path.basename(path) + '/')
            # Iterate over all items in the directory
            for item in os.listdir(path):
                # Recursively call this function for each item
                print_directory_hierarchy(os.path.join(path, item), indent + 1, extensions)
    else:
        # If it's a file, print its name only if it has the desired extension
        if path.endswith(extensions):
            print('    ' * indent + os.path.basename(path))

# Example usage
print_directory_hierarchy('/Users/mm/Desktop/courier_tracking')