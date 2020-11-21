from flask import Flask, redirect, url_for, render_template, request, session

import sqlite3
from random import random


app = Flask(__name__)

#create database and user table within
conn = sqlite3.connect('database.db')
print("Opened database successfully")

result = conn.execute("SELECT name from sqlite_master WHERE type='table' AND name='users'")

if(int(len(result.fetchall())) == 0):
	conn.execute('CREATE TABLE users (id INTEGER, name TEXT, health INTEGER)')
conn.close()

@app.route("/")
def home():

	return render_template("create_user.html")

  #return render_template("attack.html", question = "1 + 2")

if __name__ == "__main__":
	app.run(debug = True)