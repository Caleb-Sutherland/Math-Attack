from flask import Flask, redirect, url_for, render_template, request, session, g

import sqlite3
from random import random


app = Flask(__name__)
app.secret_key = "29g823fw"

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
    
@app.route("/opponents/", methods=["GET", "POST"])
def opponents():
    if request.method == 'POST':
        session['enemy'] = request.form['enemy']
        return render_template("attack.html", question = "q", enemy = session['enemy'])
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM users")
    r = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    results = []
    for row in r:
        summary = dict(zip(columns, row))
        results.append(summary)
    cursor.close()
    return render_template("opponents.html", enemies = results)

if __name__ == "__main__":
	app.run(debug = True)