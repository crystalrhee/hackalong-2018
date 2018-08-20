## Inspiration
Collective brainstorming and ideas forming on top of eachother simply lead to a pretty neat idea about linking developrs on Github together who work on the same kind of things.

## What it does
Takes your Github repo as an input and compares it's readme files against the readme files of hundreds of thousands of other repos, giving you the ones most likely to be working on similar projects to you. This allows you to find other developers working on similar projects, as well as find existing implementations of your ideas for inspiration.

## How we built it
The backend consisted of an implendation of the cosine similarity alogirthim - an algorithim that calculates the angle between two sets of text convereted into vectors based on word frequency. We implemented a scraping function that fed data into the cosine similarity algorithim in the backend, and a website front end to input the personal Github repo URL.

We downloaded over ten thousand readme's from different public repos on Github for a sample to be turned into vectors and calculated against an input.

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

## Link to Devpost Submission
https://devpost.com/software/repo-finder
