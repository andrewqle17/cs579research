import datetime as dt
import glob
import os
from urllib.parse import urlparse

import pandas as pd
from publicsuffix2 import PublicSuffixList

# Set NUM_CORES equal to number of CPU cores you are willing to use
NUM_CORES = 4
# Set DIRECTORY_PATH to point to the directory containing the list_versions directory and parsed_urls.csv
DIRECTORY_PATH = ""
os.chdir(DIRECTORY_PATH)

psl_files = glob.glob("list_versions/*.dat")
statistics = []

with open("parsed_urls.csv", "r", encoding="utf-8") as url_data, open("number_of_sites_per_psl.csv", "w", encoding="utf-8") as output:
    urls = url_data.readlines()
    urls = [url.strip() for url in urls]
    count = 0
    for psl_file in psl_files:
        psl_name = psl_file.split("\\")[1]
        file_statistics = {'date': None, 'name': psl_name, 'num_sites': 0}
        unix_time = int(psl_name.split("_")[0])
        date_time = dt.datetime.fromtimestamp(
            unix_time, tz=dt.timezone.utc)
        file_statistics['date'] = date_time
        try:
            psl = PublicSuffixList(psl_file)
        except:
            psl = PublicSuffixList(psl_file, idna=False)
        slds = pd.Series(urls).map(psl.get_sld)
        file_statistics['num_sites'] = len(slds.unique())
        output.write(
            f"{file_statistics['date']}, {file_statistics['name']}, {file_statistics['num_sites']}\n")
        count += 1
        print(f"{psl_name} processed {count}")
