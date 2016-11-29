from pymongo import MongoClient

def get_db():
    client = MongoClient('mongodb://heroku_3xjl6js5:toopv781uldifdva37t71jgd2b@ds113668.mlab.com:13668/heroku_3xjl6js5')
    db = client.heroku_3xjl6js5
    return db

