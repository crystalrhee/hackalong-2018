from flask import Flask, request, render_template, redirect
from app import app
# from app.scripts.get_json import get_repos
from app.scripts.githubWrapper import getRepoInfoFromUrl

@app.route('/')
def indes():
	return render_template('index.html')

@app.route('/', methods=['POST'])
def index_post():
	if request.method == 'POST':
		project = request.args.get('project')
	return project

@app.route('/results')
def hello_world():
	# repos = get_repos()
	repos = getRepoInfoFromUrl('https://github.com/crystalrhee/hackalong-2018')
	print(repos)
	return render_template("results.html", repos=(repos))
