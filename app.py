from flask import Flask, redirect, url_for, render_template, request, session
import sqlite3

app = Flask(__name__)

#create database and user table within
conn = sqlite3.connect('database.db')
print("Opened database successfully")

result = conn.execute("SELECT name from sqlite_master WHERE type='table' AND name='users'")
if(len(result.fetchall()) != 1):
	conn.execute('CREATE TABLE users (name TEXT, health INTEGER)')
	print("Table created successfully")
conn.close()

@app.route("/")
def home():
	return render_template("create_user.html")

if __name__ == "__main__":
	app.run(debug = True)
