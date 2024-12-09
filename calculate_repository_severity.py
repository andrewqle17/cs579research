import glob
import os
from multiprocessing import Manager, Pool

import pandas as pd
from publicsuffix2 import PublicSuffixList
from tqdm import tqdm


def calc_severity_metric(ranking_file, sites):
    alpha = 1
    beta = 9.135
    ranking_list = pd.read_csv(ranking_file, header=None)
    site_rankings = ranking_list.index[ranking_list[1].isin(sites)].tolist()
    site_rankings = [ranking+1 for ranking in site_rankings]
    severity = sum([1/(ranking + beta)**alpha for ranking in site_rankings])
    return severity


def process_psl_file(args):
    """
    Process a single PSL file and calculate the difference in SLDs.
    """
    psl_file, urls, curr_psl, ranking_file = args
    file_name = os.path.basename(psl_file)

    try:
        old_psl = PublicSuffixList(psl_file)
    except Exception:
        old_psl = PublicSuffixList(psl_file, idna=False)

    # Extract SLDs
    curr_slds = urls.map(curr_psl.get_sld)
    old_slds = urls.map(old_psl.get_sld)

    # Calculate severity
    sites = frozenset(set(curr_slds.compare(old_slds)["other"]))
    severity = calc_severity_metric(ranking_file, sites)

    return file_name, severity


def main():
    # Set NUM_CORES equal to number of CPU cores you are willing to use
    NUM_CORES = 4
    # Set DIRECTORY_PATH to point to the directory containing the list_versions directory and parsed_urls.csv
    DIRECTORY_PATH = ""
    os.chdir(DIRECTORY_PATH)

    psl_files = glob.glob("list_versions/*.dat")

    try:
        curr_psl = PublicSuffixList(psl_files[-1])
    except Exception:
        curr_psl = PublicSuffixList(psl_files[-1], idna=False)

    # Load URLs as a pandas Series
    urls = pd.read_csv("parsed_urls.csv", header=None, encoding="utf-8")[0]
    print("URLs loaded")
    ranking_file = "rankings.csv"
    # Prepare arguments for workers
    tasks = [(psl_file, urls, curr_psl, ranking_file)
             for psl_file in psl_files]

    # Use multiprocessing with tqdm
    with Pool(processes=NUM_CORES) as pool:
        results = list(tqdm(pool.imap(process_psl_file, tasks),
                       total=len(psl_files), desc="Processing PSL Files"))

    # Write results to output file
    with open("severity_per_psl_updated.csv", 'a', encoding="utf-8") as output:
        for file_name, severity in results:
            output.write(f"{file_name}, {severity}\n")
            print(f"{file_name} processed with {severity} severity")


if __name__ == "__main__":
    main()
