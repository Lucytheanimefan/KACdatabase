import re


def parseToArray(string):
	return string.split(',')

def parseName(string):
	arr = re.split(r'[,\s]',string)
	name = {'firstname':arr[0],'lastname':arr[len(arr)-1]}
	return name

def splitMajorMinor(string):
	return filter(None,re.split(r'[/\\,;\+]|\band\b|\bwith\b|\bmajor\b|\bminor\b',string))

def parseYear(string):
	print 'in parse Year-------------------'
	print string
	match = re.search('\d{4}', string)
	return match.group(0)



