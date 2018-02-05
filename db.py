import logging
import pymongo
import sys

FORMAT = "[%(levelname)s] %(message)s"
logging.basicConfig(format=FORMAT, level=logging.DEBUG, filename="gamelog.txt")
db = None
client = None

try:
    client = pymongo.MongoClient('localhost', 27017)
except pymongo.errors.ConnectionFailure as ex:
    print("Cannot connect to database")
    logging.error("Cannot connect to database")
    sys.exit(1)
except Exception as ex:
    print("Unknown exception while connecting to the mongodb: {}".format(ex))
    sys.exit(1)

try:
    db = client['euchre']
except KeyError:
    print("Database euchre does not exist.")
    sys.exit(1)