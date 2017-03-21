import os
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify, make_response
import csv
import sys
import server
from server import *
from parser import *
import sys
import json
from JSONEncoder import JSONEncoder
from queries import *
from bson.objectid import ObjectId

app = Flask(__name__)

file = open('Kick-Ass Coders Internship Application_new.csv', 'rb')
reader = csv.reader(file)
db = server.get_db()

reload(sys)
sys.setdefaultencoding('utf-8')


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
    	#resp = make_response(render_template("index.html"))
    	#resp.set_cookie('username', request.form['username'])
    	#return resp
        return render_template("index.html",username = session['name'], accountType = session['accountType'])
 
@app.route('/login', methods=['POST'])
def do_admin_login():
	name = request.form['username']
	session['name'] = name
	password = request.form['password']
	doc = db.users.find({'password':password, 'username':name})
	data = [JSONEncoder().encode(prof) for prof in doc]
	data = eval(data[0])
	if request.form['password'] == data['password'] and request.form['username'] == data['username']:
		session['accountType'] = data['accountType']
		session['logged_in'] = True
	else:
		flash('wrong password!')
	return home()

@app.route('/create_account_pg')
def create_account_pg():
	return render_template("create_account.html")

@app.route('/create_account', methods=['POST'])
def create_account():
	print request.form
	username = request.form['username']
	password = request.form['password']
	print request.form['accountType']
	db.users.insert({'username':username,'password':password,'accountType':request.form['accountType']})
	#write to database
	return home()


@app.route("/logout")
def logout():
	name = None
	session['logged_in'] = False
	return home()

@app.route("/search_page")
def search_page():
	if session.get('logged_in'):
		return render_template("search.html", accountType = session['accountType'])
	else: 
		return home()

@app.route('/search',methods=['POST','GET'])
def search():
	global db
	print "Search year: "+request.json["year"]
	data = searchWithQuery(request.json["year"], request.json["interests"], request.json["location"], request.json["word"],request.json["university"])
	return jsonify(result = data)

@app.route("/updateProfile", methods=['POST'])
def update():
	key = request.json["key"]
	new_val = request.json["value"]
	fellow_id = request.json["id"]
	db.scholarprofiles.update({'_id': ObjectId(fellow_id)}, {"$set":{key:new_val}}, upsert=True)
	return "Updated profile"
'''
@app.route('/populatedb')
def populate():
	global reader
	global db
	for row in reader:
		db.scholarprofiles.insert({
			'Email':row[1].decode('latin-1').encode('utf-8'),
			'Name':parseName(row[2].decode('latin-1').encode('utf-8')),
			'Phone':row[3].decode('latin-1').encode('utf-8'),
			'Unviersity':row[4].decode('latin-1').encode('utf-8'),
			'Graduation':row[5].decode('latin-1').encode('utf-8'),
			'Intended Major':row[6].decode('latin-1').encode('utf-8'),
			'Parsed Intended Major':splitMajorMinor(row[6].decode('latin-1').encode('utf-8')),
			'Declared Major':row[7].decode('latin-1').encode('utf-8'),
			'Relevant Coursework':parseToArray(row[8].decode('latin-1').encode('utf-8')),
			'Interested Areas of Tech':parseToArray(row[9].decode('latin-1').encode('utf-8')),
			'Interested Areas of Industry':parseToArray(row[10].decode('latin-1').encode('utf-8')),
			'Special Skills/Qualifications':row[11].decode('latin-1').encode('utf-8'),
			'Computer programming skillset':row[12].decode('latin-1').encode('utf-8'),
			'Why KAC':row[13].decode('latin-1').encode('utf-8'),
			'Interest in specific company/position':row[14].decode('latin-1').encode('utf-8'),
			'Location Preference':parseToArray(row[15].decode('latin-1').encode('utf-8')),
			'3 interesting things':row[16].decode('latin-1').encode('utf-8'),
			'Reference':row[17].decode('latin-1').encode('utf-8')
			})
'''


if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)