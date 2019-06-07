from github import Github
from threading import Thread

import argparse
import os
import pandas as pd
import numpy as np
import configparser

config = configparser.ConfigParser()

class UserStats():

    def __init__(self, df_path=None, configFile=None):
        config.read(configFile)

        self.df_path = df_path
        self.df = pd.read_csv(df_path) if os.path.exists(df_path) else pd.DataFrame(columns=['Repo', 'Views', 'Stars', 'Watching', 'Forks'])
        self.token = config["github"]["token"]
    
    def updateUserStats(self):
        df = self.df
        g = Github(self.token)

        user = g.get_user()
        print(f">>> Getting repo details of user {user.name} with GitHub url : {user.html_url} ...")
        repos = user.get_repos()

        results = [None] * repos.totalCount
        idx = 0
        threads = []
        for repo in repos:
            # Spawn a thread for each repo 
            t = Thread(target=self.updateRepoStats, args=(repo,results,idx,))
            t.start()
            threads.append(t)
            idx += 1

        # Wait for all threads to execute
        while len(threads):
            threads = [t for t in threads if t.is_alive()]

        changed = False
        # Evaluate all repo results and update output CSV accordingly
        for row in results:
            existing_entry = (df.Repo == row[0]).any()

            if existing_entry:
                if not np.array_equal(np.array(row, dtype=object), df.loc[df.Repo == row[0]].values[0]):
                    df.loc[df.Repo == row[0]] = row
                    changed=True
            else:
                df = df.append(pd.DataFrame(
                    [row], 
                    columns=['Repo', 'Views', 'Stars', 'Watching', 'Forks']), 
                    ignore_index=True
                )
                changed=True

        # Update output CSV only if it's outdated
        if changed:
            df.to_csv(f"{self.df_path}", index=None)

    def updateRepoStats(self, repo, results, idx):
        row = [
            repo.name, 
            repo.get_views_traffic()['count'], 
            repo.stargazers_count, 
            repo.watchers_count, 
            repo.forks_count
        ]
        results[idx] = row

def main():
    parser = argparse.ArgumentParser(description="Download traffic stats of a GitHub user account")
    parser.add_argument("-c", metavar="config", help="config file location", required=True)
    parser.add_argument("-o", metavar="output csv", help="output csv location", required=True)
    args = parser.parse_args()

    stats = UserStats(df_path=args.o, configFile=args.c)
    stats.updateUserStats()
    print(f">>> Successfully obtained details and saved at '{stats.df_path}'")

if __name__=='__main__':
    main()