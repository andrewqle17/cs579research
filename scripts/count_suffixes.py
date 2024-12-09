import datetime as dt
import os
from pathlib import Path

import pandas as pd

# Set NUM_CORES equal to number of CPU cores you are willing to use
NUM_CORES = 4
# Set DIRECTORY_PATH to point to the directory containing the list_versions directory and parsed_urls.csv
DIRECTORY_PATH = ""
os.chdir(DIRECTORY_PATH)
statistics = []

for filename in os.listdir():
    if filename.endswith("_public_suffix_list.dat"):
        with open(filename, "r", encoding="utf-8") as f:
            file_statistics = {'date': None, 'name': filename, 'total': 0, 1: 0, 2: 0,
                               3: 0, 4: 0, 5: 0, 6: 0, }
            unix_time = int(filename.split("_")[0])
            date_time = dt.datetime.fromtimestamp(
                unix_time, tz=dt.timezone.utc)
            file_statistics['date'] = date_time
            lines = f.readlines()
            lines = [line for line in lines if line.strip() and line[0:2]
                     != "//"]
            for line in lines:
                components = line.split('.')
                try:
                    file_statistics[len(components)] += 1
                except KeyError:
                    file_statistics[len(components)] = 1
                file_statistics['total'] += 1
            statistics.append(file_statistics)

df = pd.DataFrame(statistics).fillna(0)
df.to_csv("suffix_count_stats.csv")
