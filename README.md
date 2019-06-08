# GitHub Traffic

Like to to keep tabs on your GitHub account **traffic** stats? <br>
Fret no more.

Presenting, a GitHub traffic scraper to keep you on top of your repository traffic stats.

## A couple of essentials before kick off.
1. ***GitHub Personal Access token***! (because identity).<br>
Just generate a new token (can set it up for only **repo read** permissions); can also use an existing one. <br>
Assign it to the ***token*** variable in the **config.ini** file. <br>

```
[github]
token=<your_token>
```


2. ***Install the GitHub API***. <br>
`python install -r requirements.txt`

### Fire it up! <br>
Pass along the paths of the config file and the output csv to the program. <br>
The traffic stats of all repositories associated with the particular user are stored in the CSV. <br>
`python get_traffic.py -c config.ini -o output.csv` <br>

PS : Open to enhancements and issues. Next up, a cron job to update via email/SMS whenever there are traffic updates.

Please Star the repo if you found it interesting!
