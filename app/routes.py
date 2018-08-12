from flask import Flask, request, render_template
from app import app

@app.route('/')
@app.route('/index', methods=['POST'])
def index():
    user = {'username': 'Hackalong'}
    return render_template('index.html', title='Home', user=user)