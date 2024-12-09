#!/bin/bash

# Input file (replace with your file)
input_file="psl_version_matches.csv"
# Output file (replace with desired output file name)
output_file="known_projects.csv"

# Exclude lines containing ',Unknown'
grep -v ',Unknown' "$input_file" > "$output_file"

# Confirmation message
echo "Filtered file saved as $output_file"

