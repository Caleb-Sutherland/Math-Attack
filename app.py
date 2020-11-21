from flask import Flask, redirect, url_for, render_template, request, session
from random import random

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("attack.html", question = "1 + 2")

if __name__ == "__main__":
	app.run(debug = True)
