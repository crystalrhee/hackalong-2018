from flask import Flask, request, render_template, redirect
from app import app
from scripts import gj

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
	repos = gj.get_repos()
	return render_template("results.html", repos=(repos))