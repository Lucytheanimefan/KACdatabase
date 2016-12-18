from JSONEncoder import JSONEncoder
import server
from server import *
import re
db = server.get_db()


def interestQuery(interests):
	queries = []
	for interest in interests:
		query = {}
		query["Interested Areas of Industry"] = re.compile(".*"+interest+".*")
		queries.append(query)
	print "Interested areas of industry"
	print queries
	return queries

def query(year, interests=None):
	lasttwo = year[-2:]
	print "LAST TWO: "+lasttwo

	'''
	query = { "$or": [ { "Graduation": re.compile(".*"+year+".*") }, 
	{ "Graduation": re.compile(".*"+lasttwo+".*") } ] }
	'''

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


