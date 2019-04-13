from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask_cors import CORS
import time
from pymongo import MongoClient
import os
import copy

# Create Flask RESTful api with CORS
app = Flask(__name__)
CORS(app)
api = Api(app)

# Load DB
client = MongoClient('mongodb://admin:{}@localhost:27017/yeet'.format(os.environ["YEET_DB_PASS"]))
db = client['yeet']

# Get expiration time (in seconds) from environ or default to 12 hours
if "YEET_DB_EXPIRE" in os.environ.keys():
    expiration_seconds = int(os.environ["YEET_DB_EXPIRE"])
else:
    expiration_seconds = 12 * 60 * 60

# Load collection and set expiration
collection = db['yeets']
collection.drop_index("time_1")
collection.ensure_index("time", expireAfterSeconds=expiration_seconds)


# Define the function for the AT endpoint
class at_app(Resource):
    def get(self, yeet):
        # Add document to DB collection and return
        document = {"time": time.time(), "yeet_name": yeet, "data": request.args.get('data')}
        collection.insert_one(copy.copy(document))
        return document


# Define the function for the FROM endpoint
class from_app(Resource):
    def get(self, yeet):

        # Get most recent document with that yeet name and create response
        document = collection.find_one({"yeet_name": yeet})
        response = {"time_created": document["time"], "time_fetched": time.time(), "yeet_name": yeet, "data": document["data"]}

        # Delete document and return response
        collection.delete_one({"yeet_name": yeet})
        return response


api.add_resource(at_app, '/at/<yeet>')
api.add_resource(from_app, '/from/<yeet>')
if __name__ == '__main__':
     app.run(port='8080')
