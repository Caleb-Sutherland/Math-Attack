from os import close
from flask import Flask, redirect, url_for, render_template, request, session, g
from math import floor
import sqlite3
import random


app = Flask(__name__)
app.secret_key = "29g823fw"

DATABASE = 'database.db'

def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(DATABASE)
		cursor = db.cursor()
		cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER NOT NULL, name TEXT NOT NULL, health INTEGER NOT NULL, PRIMARY KEY(id))")
		cursor.close()
		print("success")
	return db

@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()

@app.route("/", methods=["POST", "GET"])
def home():
	if 'id' in session:
		cursor = get_db().cursor()
		result = int(cursor.execute("SELECT COUNT(health) FROM users WHERE id = "+str(session['id'])).fetchall()[0][0])
		if(result > 0):
			session['health'] = int(cursor.execute("SELECT health FROM users WHERE id = "+str(session['id'])).fetchall()[0][0])
			cursor.close()
			return redirect(url_for("opponents"))
		else:
			cursor.close()
			session.pop('id')
			return render_template("game_over.html", name=session['name'], health=session['health'])
	if(request.method == "POST"):
		cursor = get_db().cursor()
		cursor.execute("INSERT INTO users ('name', 'health') VALUES ('"+ request.form['username'] + "','100')")
		get_db().commit()
		result = cursor.execute("SELECT last_insert_rowid()")
		id = int(result.fetchall()[0][0])
		cursor.close()
		session['name'] = request.form['username']
		session['id'] = id
		session['health'] = 100
		return redirect(url_for("opponents"))
	else:
		return render_template("create_user.html", name="", health="")
	
@app.route("/opponents/", methods=["GET", "POST"])
def opponents():
	if 'id' in session:
		if request.method == 'POST':
			if 'answer' in request.form:
				enemy_health = int(session['enemy-health'])
				if floor(enemy_health/10) < 5:
					hit = 5
				else:
					hit = floor(enemy_health/10)
				if request.form['answer'] == str(session['answer']):
					cursor = get_db().cursor()
					cursor.execute("UPDATE users SET health = health + '" + str(hit) + "' WHERE id = '" + str(session['id']) + "'")
					cursor.execute("UPDATE users SET health = health - '" + str(hit) + "' WHERE id = '" + str(session['enemy']) + "'")
					cursor.execute("DELETE FROM users WHERE health <= 0")
					get_db().commit()
					cursor.close()
					return render_template("win.html", name=session['name'], health=session['health'], enemy_name = session['enemy-name'], hit = hit)
				else:
					cursor = get_db().cursor()
					cursor.execute("UPDATE users SET health = health - '" + str(hit) + "' WHERE id = '" + str(session['id']) + "'")
					cursor.execute("DELETE FROM users WHERE health <= 0")
					get_db().commit()
					cursor.close()
					return render_template("loss.html", name=session['name'], health=session['health'], hit = hit)
			session['enemy'] = request.form['enemy']
			session['enemy-name'] = request.form['enemy-name']
			session['enemy-health'] = request.form['enemy-health']
			question, session['answer'] = questionGenerator()
			return render_template("attack.html", name=session['name'], health=session['health'], question = question, enemy = session['enemy'], enemy_name = session['enemy-name'], enemy_health = int(session['enemy-health']))
		cursor = get_db().cursor()
		cursor.execute("SELECT * FROM users ORDER BY health DESC")
		r = cursor.fetchall()
		columns = [desc[0] for desc in cursor.description]
		results = []
		for row in r:
			summary = dict(zip(columns, row))
			results.append(summary)
		cursor.close()
		highest = results[0]['health']
		return render_template("opponents.html", name=session['name'], health=session['health'], enemies = results, id = session['id'], highest=highest)
	else:
		return redirect(url_for("home"))

@app.route("/admin/", methods=["GET", "POST"])
def admin():
	if 'name' in request.form:
		cursor = get_db().cursor()
		cursor.execute("INSERT INTO users ('name', 'health') VALUES ('"+ request.form['name'] + "','100')")
		get_db().commit()
		cursor.close()
		return "<form method='POST'><input name='name'></form>"
	else:
		return "<form method='POST'><input name='name'></form>"
	


	#0-50 50-70 70-90 90-110 110-130 130-150 150-+
	#under 50 is 1 digit numbers just one operation
	#1 digit numbers 2 operations
	#2 digit numbers 2 operations

def questionGenerator():
	cursor = get_db().cursor()
	result = int(cursor.execute("SELECT health FROM users WHERE id = "+str(session['enemy'])).fetchall()[0][0])
	question = ""
	answer = 0
	if(result < 50):
		d1 = random.randint(1, 9)
		d2 = random.randint(1, 9)		
		selector = random.randint(1, 4)
		if(selector == 1):
			question = str(d1) + " + " + str(d2) + " = "
			answer = d1 + d2
		elif(selector == 2):
			question = str(d1) + " - " + str(d2) + " = "
			answer = d1 - d2
		elif(selector == 3):
			while(d1%d2 != 0):
				d1 = random.randint(1, 9)
				d2 = random.randint(1, 9)
			question = str(d1) + " / " + str(d2) + " = "
			answer = d1/d2
		elif(selector == 4):
			question = str(d1) + " x " + str(d2) + " = "
			answer = d1*d2

	elif(result >= 50 and result < 70):
		d1 = random.randint(1, 9)
		d2 = random.randint(1, 9)
		d3 = random.randint(1, 9)
		selector = random.randint(1, 4)
		if(selector == 1):
			question = str(d1) + " + " + str(d2) + " - " + str(d3) + " = "
			answer = d1 + d2 - d3
		elif(selector == 2):
			question = str(d1) + " - " + str(d2) + " x " + str(d3) + " = "
			answer = d1 - (d2 * d3)
		elif(selector == 3):
			while(d1%d2 != 0):
				d1 = random.randint(1, 9)
				d2 = random.randint(1, 9)
			question = str(d1) + " / " + str(d2) + " + " + str(d3) + " = "
			answer = (d1/d2) + d3
		elif(selector == 4):
			question = str(d1) + " x " + str(d2) + " - " + str(d3) + " = "
			answer = (d1*d2) - d3

	elif(result >= 70 and result < 90):
		d1 = random.randint(5, 12)
		d2 = random.randint(5, 12)
		d3 = random.randint(1, 9)
		selector = random.randint(1, 4)
		if(selector == 1):
			question = str(d1) + " + " + str(d2) + " - " + str(d3) + " = "
			answer = d1 + d2 - d3
		elif(selector == 2):
			question = str(d1) + " - " + str(d2) + " x " + str(d3) + " = "
			answer = d1 - (d2 * d3)
		elif(selector == 3):
			while(d1%d2 != 0):
				d1 = random.randint(5, 12)
				d2 = random.randint(5, 12)
			question = str(d1) + " / " + str(d2) + " + " + str(d3) + " = "
			answer = (d1/d2) + d3
		elif(selector == 4):
			question = str(d1) + " x " + str(d2) + " - " + str(d3) + " = "
			answer = (d1*d2) - d3

	elif(result >= 90 and result < 110):
		d1 = random.randint(5, 19)
		d2 = random.randint(5, 19)
		d3 = random.randint(1, 9)
		selector = random.randint(1, 4)
		if(selector == 1):
			question = str(d1) + " + " + str(d2) + " - " + str(d3) + "^2 = "
			answer = d1 + d2 - (d3**2)
		elif(selector == 2):
			question = str(d1) + "^2 - " + str(d2) + " x " + str(d3) + " = "
			answer = (d1**2) - (d2 * d3)
		elif(selector == 3):
			while(d1%d2 != 0):
				d1 = random.randint(5, 19)
				d2 = random.randint(5, 19)
			question = str(d1) + " / " + str(d2) + " - " + str(d3) + "^2 = "
			answer = (d1/d2) - (d3**2)
		elif(selector == 4):
			question = str(d1) + " x " + str(d2) + " + " + str(d3) + "^2 = "
			answer = (d1*d2) + (d3**2)

	elif(result >= 110 and result < 130):
		d1 = random.randint(5, 19)
		d2 = random.randint(5, 19)
		d3 = random.randint(5, 19)
		selector = random.randint(1, 4)
		if(selector == 1):
			question = str(d1) + " + " + str(d2) + " - " + str(d3) + " = "
			answer = d1 + d2 - (d3)
		elif(selector == 2):
			question = str(d1) + " x " + str(d2) + " - " + str(d3) + " = "
			answer = (d1 * d2) - d3
		elif(selector == 3):
			while(d1%d2 != 0):
				d1 = random.randint(5, 19)
				d2 = random.randint(5, 19)
			question = str(d1) + " / " + str(d2) + " - " + str(d3) + " = "
			answer = (d1/d2) - (d3)
		elif(selector == 4):
			question = str(d1) + " x " + str(d2) + " + " + str(d3) + " = "
			answer = (d1*d2) + (d3)

	elif(result >= 130 and result < 150):
		d1 = random.randint(11, 29)
		d2 = random.randint(11, 29)
		d3 = random.randint(11, 29)
		selector = random.randint(1, 4)
		if(selector == 1):
			question = str(d1) + " + " + str(d2) + " - " + str(d3) + " = "
			answer = d1 + d2 - (d3)
		elif(selector == 2):
			question = str(d1) + " x " + str(d2) + " - " + str(d3) + " = "
			answer = (d1 * d2) - d3
		elif(selector == 3):
			while(d1%d2 != 0):
				d1 = random.randint(11, 29)
				d2 = random.randint(11, 29)
			question = str(d1) + " / " + str(d2) + " - " + str(d3) + " = "
			answer = (d1/d2) - (d3)
		elif(selector == 4):
			question = str(d1) + " x " + str(d2) + " + " + str(d3) + " = "
			answer = (d1*d2) + (d3)

	else:
		d1 = random.randint(11, 39)
		d2 = random.randint(11, 39)
		d3 = random.randint(11, 39)
		d4 = random.randint(11, 39)
		selector = random.randint(1, 4)
		if(selector == 1):
			question = str(d1) + " + " + str(d2) + " - " + str(d3) + " x " + str(d4) + " = "
			answer = d1 + d2 - (d3*d4)
		elif(selector == 2):
			while(d3%d4 != 0):
				d3 = random.randint(11, 39)
				d4 = random.randint(11, 39)
			question = str(d1) + " x " + str(d2) + " - " + str(d3) + " / " + str(d4) + " = "
			answer = (d1 * d2) - (d3/d4)
		elif(selector == 3):
			while(d1%d2 != 0):
				d1 = random.randint(11, 39)
				d2 = random.randint(11, 39)
			question = str(d1) + " / " + str(d2) + " - " + str(d3) + " x " + str(d4) + " = "
			answer = (d1/d2) - (d3*d4)
		elif(selector == 4):
			question = str(d1) + " x " + str(d2) + " + " + str(d3) + " x " + str(d4) + " = "
			answer = (d1*d2) + (d3*d4)

	return question, int(answer)


if __name__ == "__main__":
	app.run(debug = True)