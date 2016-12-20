from JSONEncoder import JSONEncoder
import server
from server import *
import re
db = server.get_db()


def listQuery(interests, keyLabel):
	queries = []
	print interests
	for interest in interests:
		query = {}
		query[keyLabel] = {"$in":[re.compile("(?:^|\W)"+interest+"(?:$|\W)",re.IGNORECASE)]}
		queries.append(query)
	if (len(interests)<1):
		query = {}
		query[keyLabel]={"$in":[re.compile(".*",re.IGNORECASE)]}
		queries.append(query)
	return queries

def textSearchQuery(word):
	#"Computer programming skillset"
	#"Special Skills/Qualifications"
	if (word is None or len(word)<1):
		wordRegex = ".*"
	else:
		wordRegex = ".*"+word+".*"
	query = []
	queries={}
	query.append({"Computer programming skillset":re.compile(wordRegex,re.IGNORECASE)})
	query.append({"Special Skills/Qualifications":re.compile(wordRegex,re.IGNORECASE)})
	query.append({"3 interesting things":re.compile(wordRegex,re.IGNORECASE)})
	queries["$or"]=query
	return queries


def query(year, interests=None, locationPref=None, word=None):
	lasttwo = year[-2:]

	#error checking for empty values
	if year is None or len(year)<4:
		gradRegex = ".*"
	else:
		gradRegex = ".*"+year+".*"

	if locationPref is None or len(locationPref)<1:
		locationPrefRegex = ".*"
	else:
		locationPrefRegex = ".*"+locationPref+".*"

	query = {"$and" : [{ "$or": [ { "Graduation": re.compile(gradRegex) }, 
	{ "Graduation": re.compile(".*"+lasttwo+".*") } ] },
	{"$or":listQuery(interests,"Interested Areas of Tech")},
	{"Location Preference":re.compile(locationPrefRegex)},
	textSearchQuery(word)]}
	
	print "QUERY"
	print query

	return query


def searchWithQuery(year, interests, locationPref, word):
	global db
	lasttwo = year[-2:]
	doc = db.scholarprofiles.find(query(year, interests, locationPref, word))

	print '-------------------CURSOR------------'
	data = [JSONEncoder().encode(prof) for prof in doc]
	print data
	return data


