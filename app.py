from flask import Flask, redirect, url_for, render_template, request, session

import sqlite3
from random import random


app = Flask(__name__)

#create database and user table within
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
print("Opened database successfully")

result = cursor.execute("SELECT name from sqlite_master WHERE type='table' AND name='users'")

if(int(len(result.fetchall())) == 0):
	cursor.execute('CREATE TABLE users (id INTEGER NOT NULL, name TEXT NOT NULL, health INTEGER NOT NULL, PRIMARY KEY(id))')
cursor.close()

@app.route("/")
def home():

	return render_template("create_user.html")

  #return render_template("attack.html", question = "1 + 2")

if __name__ == "__main__":
	app.run(debug = True)