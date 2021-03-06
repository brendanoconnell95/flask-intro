# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request,\
    session, flash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import os

# create the application object
app = Flask(__name__)

#configuration settings
app.config.from_object(os.environ['APP_SETTINGS'])

#create the sql alchemy objet
db = SQLAlchemy(app)

from models import *
# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

# use decorators to link the function to a url
@app.route('/')
@login_required
def home():
    #return "Hello, World!"  # return a string
    posts = db.session.query(BlogPost).all()
    return render_template('index.html', posts=posts)
    
@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash('You were just logged in!')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/logout') 
@login_required
def logout(): 
    session.pop('logged_in', None)
    flash('You were just logged out!')
    return redirect(url_for('welcome'))

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run()