import os
import string
import random

def generate_random_string(length):
  """Generates a random string of the specified length."""
  chars = string.ascii_lowercase + string.digits
  return ''.join(random.choice(chars) for _ in range(length))

def create_file(folder_path, filename, content):
  """Creates a file with the given filename and content in the specified folder."""
  filepath = os.path.join(folder_path, filename)
  with open(filepath, 'w') as f:
    f.write(content)

def main():
  # Get the number of files to generate from the user
  num_files = int(input("Enter the number of files to generate: "))

  # Specify the folder path
  folder_path = "important-stuff"  # Replace with your desired folder path

  # Create the folder if it doesn't exist
  if not os.path.exists(folder_path):
    os.makedirs(folder_path)

  # Generate and create files
  for _ in range(num_files):
    filename = generate_random_string(8)
    content = generate_random_string(8)
    create_file(folder_path, filename, content)

  print(f"{num_files} files generated in {folder_path}")

if __name__ == "__main__":
  main()
