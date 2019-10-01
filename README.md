# GitHub Traffic

Like to to keep tabs on your GitHub account **traffic** statistics? <br>
Fret no more.

Presenting, a GitHub traffic scraper to keep you on top of your repository traffic stats.

## A couple of pre-requisites before you kick off.
1. ***GitHub Personal Access token***! (because identity).<br>
Just generate a new token (can set it up for only **repo read** permissions); you can also use an existing one. <br>
Assign it to ***token*** in the **config.ini** file. <br>

```
[github]
token=<personal_access_token>
```


2. ***Install the official python GitHub package (pyGithub) and pandas***. <br>
`pip install -r requirements.txt`

### Fire it up! <br>
`python get_traffic.py` <br>
The traffic stats of all repositories associated with the user are stored in the CSV `<user_name>.csv`. <br>

PS : Open to your suggestions and enhancements. Plan to make it a cron job that regularly updates you of the current traffic!

Please Star the repo if you found it interesting!
