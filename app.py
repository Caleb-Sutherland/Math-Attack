from flask import Flask, redirect, url_for, render_template, request, session, g

import sqlite3
from random import random


app = Flask(__name__)

DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def home():

	return render_template("create_user.html")

  #return render_template("attack.html", question = "1 + 2")
    
@app.route("/check/")
def check():
    result = get_db().execute("SELECT name FROM users")
    value = str(result.fetchall())
    return value

if __name__ == "__main__":
	app.run(debug = True)