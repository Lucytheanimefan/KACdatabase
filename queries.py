from JSONEncoder import JSONEncoder
import server
from server import *

db = server.get_db()


def yearQuery(year):
	lasttwo = year[-2:]
	print "LAST TWO: "+lasttwo
	query = { "$or": [ { "Graduation": {"$regex" : ".*"+year+".*"} }, { "Graduation": {"$regex" : ".*"+lasttwo+".*"} } ] }
	print query
	return query


def search(year):
	global db
	lasttwo = year[-2:]
	doc = db.scholarprofiles.find(yearQuery(year))
	'''
	for pro in doc:
		print type(pro)
		data.append(dict(pro))
	'''
	print '-------------------CURSOR------------'
	data = [JSONEncoder().encode(prof) for prof in doc]
	print data
	return data



search("2019")



