from JSONEncoder import JSONEncoder
import server
from server import *
import re
db = server.get_db()


def interestQuery(interests):
	queries = []
	print interests
	for interest in interests:
		print "Interest: "+interest
		query = {}
		query["Interested Areas of Tech"] = {"$in":[re.compile("(?:^|\W)"+interest+"(?:$|\W)",re.IGNORECASE)]}
		queries.append(query)
	print "Interested Areas of Tech"
	print queries
	return queries

def query(year, interests=None):
	lasttwo = year[-2:]
	print "LAST TWO: "+lasttwo

	'''
	query = { "$or": [ { "Graduation": re.compile(".*"+year+".*") }, 
	{ "Graduation": re.compile(".*"+lasttwo+".*") } ] }
	'''
	if len(interests)<=0:
		query = { "$or": [ { "Graduation": re.compile(".*"+year+".*") }, { "Graduation": re.compile(".*"+lasttwo+".*") } ] }
	else:
		query = {"$and" : [{ "$or": [ { "Graduation": re.compile(".*"+year+".*") }, 
		{ "Graduation": re.compile(".*"+lasttwo+".*") } ] },
		{"$or":interestQuery(interests)}]}
	
	print query
	return query


def searchWithQuery(year, interests):
	global db
	lasttwo = year[-2:]
	doc = db.scholarprofiles.find(query(year, interests))

	print '-------------------CURSOR------------'
	data = [JSONEncoder().encode(prof) for prof in doc]
	print data
	return data


