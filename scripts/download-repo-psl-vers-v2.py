import csv
import requests
import os

# Path to the CSV file and output directory
csv_path = 'sourcegraph-search-export-context-global-file-public_suffix_list-dat.csv'
output_dir = './downloaded_files'
MAXDOWNLOADS = 500
os.makedirs(output_dir, exist_ok=True)

# Function to construct the filename
def create_filename(repo_name):
    parts = repo_name.split('/')
    if len(parts) >= 3:
        return f"{parts[1]}_{parts[2]}"
    else:
        raise ValueError("Unexpected repository format")

# Function to modify the File URL
def modify_file_url(file_url):
    return file_url.replace('/blob/', '/raw/', 1)

# Read the CSV and download files
with open(csv_path, 'r') as file:
    reader = csv.DictReader(file)
    for i, row in enumerate(reader):
        if i >= MAXDOWNLOADS:  # Stop after the first 5 rows
            break

        # Extract fields
        repo_name = row['Repository']
        file_url = row['File URL']

        # Modify the File URL to the raw format and construct the output filename
        raw_file_url = modify_file_url(file_url)
        filename = create_filename(repo_name)
        output_path = os.path.join(output_dir, f"{filename}.dat")

        # Download the file
        try:
            response = requests.get(raw_file_url)
            response.raise_for_status()
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {raw_file_url} to {output_path}")
        except requests.HTTPError as e:
            print(f"Failed to download {raw_file_url}: {e}")

print("Download complete.")

