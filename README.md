Hackathon Project for Hackalong

## Setting up virtualenv

In a different folder outside of the repo. This will create a virtuel environment folder for setting up the project

`virtualenv -p python3 venv`

activate the environment

`. ./venv/bin/activate`

`cd` back to the repo. Install all the requirements for this project

`pip install -r requirements.txt`

Run the flask server

`flask run`


## Running the core python script on command line
### Obtaining github API token
`cd app/scripts`

head to github's [developer settings](https://github.com/settings/tokens) to obtain an API token. (make sure `public_repo` is checked)

replace `GITHUB_TOKEN` in `config.py` with your newly generated token.

### Running public repo fetcher
Once api token is setup, run the repo fetcher by doing this (make sure your in the virtualenv, using python3)

`python repoFetcher.py`

this will keep going until it crashes or it finished downloading Github, feel free to cancel (`control+c`) anytime, output will be saved to `readmes.csv`

### Convert plain readme text to a dictionary or "vectors"
Run this, output will be saved to `scores.csv`

`python textToDict.py`

### Find the top similar repos
Run this, output will be printed in console if `debug` is set to `true` in `__main__`

`python cosineComparison.py`


