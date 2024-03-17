import os
project_dir = "/Users/mm/Desktop/courier_tracking" 
# Define the path to the directory
directory_path = project_dir  # Replace 'project_dir' with the actual directory path

# Define a list of target file names to match
target_file_names = [
    "models.py",
    "views.py",
    "urls.py",
    "settings.py",
    "manage.py",
    "apps.py",
    "admin.py",
    "forms.py",
    "backends.py",
]

# Iterate through the directory and its subdirectories
for root, _, files in os.walk(directory_path):
    for file_name in files:
        if file_name.endswith('.html') or file_name in target_file_names:
            full_path = os.path.join(root, file_name)
            with open(full_path, "r") as file:
                print(f"Contents of {full_path}:")
                print(file.read())
                print("\n" + "=" * 50 + "\n")  # Separating lines for readability