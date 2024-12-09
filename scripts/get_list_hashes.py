import datetime as dt
import glob
import hashlib
import os
import subprocess
from pathlib import Path

import pandas as pd


def get_list_hash(psl_filename):
    git_hash = subprocess.run(
        ['git', 'hash-object', psl_filename], stdout=subprocess.PIPE)
    git_hash = str(git_hash.stdout)[2:-3]
    return git_hash


def main():
    BUFFER_SIZE = 65536
    DIRECTORY_PATH = "D:\.Homework\CS579\Research\our_work\data"

    os.chdir(DIRECTORY_PATH)
    psl_files = glob.glob("list_versions/*.dat")
    statistics = []

    for psl_file in psl_files:
        file_name = psl_file.split('\\')[1]
        file_statistics = {'name': file_name, 'hash': get_list_hash(psl_file)}
        # with open(psl_file, mode='rb') as f:
        #     sha1 = hashlib.sha1()
        #     sha256 = hashlib.sha256()
        #     while True:
        #         data = f.read(BUFFER_SIZE)
        #         if not data:
        #             break
        #         sha1.update(data)
        #         sha256.update(data)
        #     file_statistics['sha1'] = sha1.hexdigest()
        #     file_statistics['sha256'] = sha256.hexdigest()
        statistics.append(file_statistics)
    pd.DataFrame(statistics).to_csv("psl_list_hashes.csv")


if __name__ == "__main__":
    main()
