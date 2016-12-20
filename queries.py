from JSONEncoder import JSONEncoder
import server
from server import *
import re
db = server.get_db()


def listQuery(interests, keyLabel):
	queries = []
	print interests
	for interest in interests:
		print "Interest: "+interest
		query = {}
		query[keyLabel] = {"$in":[re.compile("(?:^|\W)"+interest+"(?:$|\W)",re.IGNORECASE)]}
		queries.append(query)
	if (len(interests)<1):
		query = {}
		query[keyLabel]={"$in":[re.compile(".*",re.IGNORECASE)]}
		queries.append(query)
	print "keyLabel"
	print queries
	return queries

def query(year, interests=None, locationPref=None):
	lasttwo = year[-2:]
	print "LAST TWO: "+lasttwo

	#error checking for empty values
	if year is None or len(year)<4:
		gradRegex = ".*"
	else:
		gradRegex = ".*"+year+".*"

	if locationPref is None or len(locationPref)<1:
		locationPrefRegex = ".*"
	else:
		locationPrefRegex = ".*"+locationPref+".*"

	#if len(interests)<=0:
	#	query = { "$or": [ { "Graduation": re.compile(gradRegex) }, { "Graduation": re.compile(".*"+lasttwo+".*") } ] }
	#else:
	query = {"$and" : [{ "$or": [ { "Graduation": re.compile(gradRegex) }, 
	{ "Graduation": re.compile(".*"+lasttwo+".*") } ] },
	{"$or":listQuery(interests,"Interested Areas of Tech")},
	{"Location Preference":re.compile(locationPrefRegex)}]}
	
	print query
	return query


def searchWithQuery(year, interests, locationPref):
	global db
	lasttwo = year[-2:]
	doc = db.scholarprofiles.find(query(year, interests, locationPref))

	print '-------------------CURSOR------------'
	data = [JSONEncoder().encode(prof) for prof in doc]
	print data
	return data


