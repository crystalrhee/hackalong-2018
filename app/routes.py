from flask import Flask, request, render_template
from app import app
import json

@app.route('/')
@app.route('/index', methods=['POST'])
def index():
	# if form.validate():
	# 	return redirect(url_for('results'))
	# else:
	return render_template('index.html')

def get_repos():
	repos = [{"name": "repo1", "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.", "last_updated": 3, "link": "https://github.com/"},
	{"name": "repo2", "description": "some description", "last_updated": 3, "link": "https://github.com/"},
	{"name": "repo3", "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.", "last_updated": 3, "link": "https://github.com/"},
	{"name": "repo4", "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.", "last_updated": 3, "link": "https://github.com/"},
	{"name": "repo5", "description": "some description", "last_updated": 3, "link": "https://github.com/"},
	{"name": "repo6", "description": "some description", "last_updated": 3, "link": "https://github.com/"}]
	return repos

@app.route('/results')
def hello_world():
	repos = get_repos()
	return render_template("results.html", repos=(repos)) 