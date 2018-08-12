from flask import Flask, request, render_template
from app import app
from scripts import gj

@app.route('/')
@app.route('/index', methods=['POST'])
def index():
	# if form.validate():
	# 	return redirect(url_for('results'))
	# else:
	return render_template('index.html')

@app.route('/results')
def hello_world():
	repos = gj.get_repos()
	return render_template("results.html", repos=(repos)) 