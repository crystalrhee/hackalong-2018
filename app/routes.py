from app import app
from flask import Flask, request, render_template

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Hackalong'}
    return render_template('index.html', title='Home', user=user)