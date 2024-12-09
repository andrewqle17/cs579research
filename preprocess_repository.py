import pandas as pd

repo_stats = pd.read_csv("our_work/data/repository_statistics.csv")
severity_stats = pd.read_csv(
    "our_work/data/severity_per_psl.csv", header=None, names=['psl', 'severity']).set_index('psl')['severity'].to_dict()


repo_stats = repo_stats[repo_stats["Matched Version"] != "Unknown"]
repo_stats["Static or Dynamic"] = repo_stats["Static or Dynamic"].str.lower()
repo_stats["Matched Version"] = repo_stats["Matched Version"].str.strip()
repo_stats['severity'] = repo_stats["Matched Version"].map(severity_stats)
repo_stats.to_csv("proc_repo_stats.csv")
