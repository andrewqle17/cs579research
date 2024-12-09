import csv
from datetime import datetime
import matplotlib.pyplot as plt

# Input CSV file
input_file = "psl_version_matches - Sheet1.csv"

# Initialize lists for ages of repositories
ages_static = []
ages_dynamic = []
ages_total = []  # To store combined ages

# Get current date (or specify any reference date for age calculation)
current_date = datetime.utcnow().date()

# Read and process the CSV file
with open(input_file, "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        matched_version = row.get("Matched Version", "")
        static_or_dynamic = row.get("Static or Dynamic", "").lower()  # Get Static or Dynamic field and convert to lowercase
        # Extract Unix timestamp if it starts with a numeric string
        if matched_version and matched_version[0].isdigit():
            try:
                timestamp = int(matched_version.split("_")[0])  # Extract first numeric part
                release_date = datetime.utcfromtimestamp(timestamp).date()  # Convert timestamp to release date
                
                # Calculate the age of the repository
                age = (current_date - release_date).days  # Age in days
                
                # Append age to corresponding list based on static or dynamic classification
                if static_or_dynamic == "static":
                    ages_static.append(age)
                    ages_total.append(age)  # Add to total list
                elif static_or_dynamic == "dynamic":
                    ages_dynamic.append(age)
                    ages_total.append(age)  # Add to total list
            except ValueError:
                continue

# Sort the ages for cumulative distribution calculation
ages_static.sort()
ages_dynamic.sort()
ages_total.sort()  # Sort the total ages as well

# Calculate cumulative counts
cumulative_static = list(range(1, len(ages_static) + 1))
cumulative_dynamic = list(range(1, len(ages_dynamic) + 1))
cumulative_total = list(range(1, len(ages_total) + 1))

# Calculate the proportions (cumulative count / total projects of that type)
proportion_static = [count / len(ages_static) for count in cumulative_static]
proportion_dynamic = [count / len(ages_dynamic) for count in cumulative_dynamic]
proportion_total = [count / len(ages_total) for count in cumulative_total]  # Proportion for total

# Plot cumulative distribution of static, dynamic, and total projects as proportions
plt.figure(figsize=(10, 6))

# Static Projects (cumulative distribution as proportion)
plt.plot(ages_static, proportion_static, marker="o", linestyle="-", color="blue", label="Static")

# Dynamic Projects (cumulative distribution as proportion)
plt.plot(ages_dynamic, proportion_dynamic, marker="o", linestyle="-", color="green", label="Dynamic")

# Total Projects (cumulative distribution as proportion)
plt.plot(ages_total, proportion_total, marker="o", linestyle="-", color="purple", label="Total")

# Customize the plot
plt.title("Relative PSL age:\nList age vs. latest (days)", fontsize=14)
plt.xlabel("Age (in days)", fontsize=12)
plt.ylabel("Proportion of Projects (CDF)", fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.legend()

# Show the plot
plt.show()

