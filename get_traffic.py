from github import Github
from multiprocessing import Pool, Process

import configparser
import pandas as pd

config_file = 'config.ini'
config = configparser.ConfigParser()

class GithubTraffic():
    """
    Class that extracts the repo traffic stats of a github user
    """

    def __init__(self, token):
    
        self.token = token

        self.get_user()

    def get_user(self):
        """
        Gets the user using the Personal Access token
        """

        g = Github(self.token)

        self.user = g.get_user()
        self.user_name = self.user.login

    def get_user_repos(self):
        """
        Gets all the repos of the user
        """

        return self.user.get_repos()

    @staticmethod
    def get_repo_stats(repo):
        """
        Get the stats of the repo.
        Ideally should be parallelized because the `repo.get_views_traffic()` method is blocking.
        """

        return {
                'Repository' : repo.full_name,
                'Views'      : repo.get_views_traffic()['count'],
                'Stars'      : repo.stargazers_count,
                'Watchers'   : repo.watchers_count,
                'Forks'      : repo.forks_count,
                'Clones'     : repo.get_clones_traffic()['count']
            }

    def update_traffic_stats(self):
        """
        Get the latest traffic stats for the user
        """

        print(f"Extracting repo stats of '{self.user_name}'...")

        p = Pool(5)
        repos_stats = p.map(GithubTraffic.get_repo_stats, self.get_user_repos())
        print(f"Extracted {len(repos_stats)} repos!\n")

        print("Saving the repo stats...")

        df_handler = DFHandler(username=self.user_name)
        df_handler.save(stats=repos_stats)
        print(f"Successfully saved to {df_handler.csv}")

class DFHandler():

    def __init__(self, username=None):

        self.csv = f'{username}.csv'

    def save(self, stats):
        """
        Save the repo stats to a CSV
        """

        df = pd.DataFrame(stats)
        df.to_csv(self.csv, index=False)

if __name__=='__main__':

    config.read(config_file)
    token = config['github']['token'] 

    traffic_client = GithubTraffic(token)
    traffic_client.update_traffic_stats()