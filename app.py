import os
from flask import Flask
from flask import render_template,jsonify, request
import csv
import sys
import server
from server import *
from parser import *
import sys
import json
from JSONEncoder import JSONEncoder
from queries import *

app = Flask(__name__)

file = open('Kick-Ass Coders Internship Application_new.csv', 'rb')
reader = csv.reader(file)
db = server.get_db()

reload(sys)
sys.setdefaultencoding('utf-8')


@app.route("/")
@app.route("/home")
@app.route("/search")
def home():
	return render_template('search.html')


@app.route('/search',methods=['POST','GET'])
def search():
	global db
	print "Search year: "+request.json["year"]
	data = searchWithQuery(request.json["year"])
	return jsonify(result = data)

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
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)