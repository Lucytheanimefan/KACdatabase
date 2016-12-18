from JSONEncoder import JSONEncoder
import server
from server import *
import re
db = server.get_db()


def yearQuery(year):
	lasttwo = year[-2:]
	print "LAST TWO: "+lasttwo
	query = { "$or": [ { "Graduation": re.compile(".*"+year+".*") }, { "Graduation": re.compile(".*"+lasttwo+".*") } ] }
	print query
	return query


def searchWithQuery(year):
	global db
	lasttwo = year[-2:]
	doc = db.scholarprofiles.find(yearQuery(year))

	print '-------------------CURSOR------------'
	data = [JSONEncoder().encode(prof) for prof in doc]
	print data
	return data



searchWithQuery("2019")

