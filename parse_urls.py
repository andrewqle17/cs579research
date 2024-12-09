import os
from urllib.parse import urlparse

# Set NUM_CORES equal to number of CPU cores you are willing to use
NUM_CORES = 4
# Set DIRECTORY_PATH to point to the directory containing the list_versions directory and parsed_urls.csv
DIRECTORY_PATH = ""
os.chdir(DIRECTORY_PATH)

with open("urls.csv", "r", encoding="utf-8") as f, open("parsed_urls.csv", "w", encoding="utf-8") as o:
    urls = f.readlines()
    urls = [url.split(',')[1].strip() for url in urls[1:]]
    parsed = [urlparse(url).hostname for url in urls]
    for url in parsed:
        o.write(f'{url}\n')
