#!/bin/bash

# Input file (replace with your file)
input_file="psl_unknowns.csv"
# Output file (replace with desired output file name)
output_file="unknown_projects_cleaned.txt"

# Process the file
awk -F',' '{print $1}' "$input_file" > "$output_file"

# Confirmation message
echo "Processed file saved as $output_file"

