import os
import hashlib
import csv

# Directories
project_psl_dir = './project_text_psls'  # Replace with your project PSLs folder
historic_psl_dir = './historic_psls'  # Replace with your historic PSLs folder
output_csv = 'psl_version_matches.csv'

# Function to calculate file hash, ignoring whitespace
def calculate_file_hash(filepath):
    """Calculate the hash of a file with whitespace and comments removed."""
    hash_md5 = hashlib.md5()
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            # Remove comments and strip whitespace
            line = line.split('//', 1)[0].strip()
            if line:  # Ignore empty lines after processing
                hash_md5.update(line.encode('utf-8'))
    
    return hash_md5.hexdigest()

# Build a hash-to-filename mapping for the historic PSLs
historic_hashes = {}
print("Starting historic hashing")
for historic_file in os.listdir(historic_psl_dir):
    #print(f"Analyzing {historic_file}")
    historic_path = os.path.join(historic_psl_dir, historic_file)
    if os.path.isfile(historic_path):
        file_hash = calculate_file_hash(historic_path)
        historic_hashes[file_hash] = historic_file

# Compare each project PSL against historic versions
matches = []
print(f"Starting project hashing")
for project_file in os.listdir(project_psl_dir):
    #print(f"Analyzing {project_file}")
    project_path = os.path.join(project_psl_dir, project_file)
    if os.path.isfile(project_path):
        project_hash = calculate_file_hash(project_path)
        matched_version = historic_hashes.get(project_hash, "Unknown")
        matches.append({'Project PSL': project_file, 'Matched Version': matched_version})

# Write the results to a CSV
with open(output_csv, 'w', newline='') as csvfile:
    fieldnames = ['Project PSL', 'Matched Version']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(matches)

print(f"CSV created: {output_csv}")

