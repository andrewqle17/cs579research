import glob
import os
from multiprocessing import Manager, Pool

import pandas as pd
from publicsuffix2 import PublicSuffixList
from tqdm import tqdm


def process_psl_file(args):
    """
    Process a single PSL file and calculate the difference in SLDs.
    """
    psl_file, urls, curr_psl = args
    file_name = os.path.basename(psl_file)

    try:
        old_psl = PublicSuffixList(psl_file)
    except Exception:
        old_psl = PublicSuffixList(psl_file, idna=False)

    # Extract SLDs
    curr_slds = urls.map(curr_psl.get_sld)
    old_slds = urls.map(old_psl.get_sld)

    # Compare and count differences
    sld_diff = curr_slds.compare(old_slds)
    print(sld_diff)
    diff_url_count = len(sld_diff['other'].unique())
    return file_name, diff_url_count


def main():
    # Set NUM_CORES equal to number of CPU cores you are willing to use
    NUM_CORES = 4
    # Set DIRECTORY_PATH to point to the directory containing the list_versions directory and parsed_urls.csv
    DIRECTORY_PATH = "our_work/data"
    os.chdir(DIRECTORY_PATH)

    psl_files = glob.glob("list_versions/*.dat")[-20:]

    try:
        curr_psl = PublicSuffixList(psl_files[-1])
    except Exception:
        curr_psl = PublicSuffixList(psl_files[-1], idna=False)

    # Load URLs as a pandas Series
    urls = pd.read_csv("parsed_urls.csv", header=None, encoding="utf-8")[0]
    print("URLs loaded")

    # Prepare arguments for workers
    tasks = [(psl_file, urls, curr_psl) for psl_file in psl_files]

    # Use multiprocessing with tqdm
    with Pool(processes=NUM_CORES) as pool:
        results = list(tqdm(pool.imap(process_psl_file, tasks),
                       total=len(psl_files), desc="Processing PSL Files"))

    # Write results to output file
    # with open("misclassified_sites_per_psl.csv", 'a', encoding="utf-8") as output:
    #     for file_name, diff_site_count in results:
    #         output.write(f"{file_name}, {diff_site_count}\n")
    #         print(f"{file_name} processed with {diff_site_count} differences")


if __name__ == "__main__":
    main()
