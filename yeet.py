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


# Define the function for the TO endpoint
class to_app(Resource):
    def get(self, yeet):
        # Add document to DB collection
        document = {"time": time.time(), "yeet_name": yeet, "data": request.args.get('data')}
        collection.insert_one(copy.copy(document))

        # Return document with success message
        document["success"] = True
        return document


# Define the function for the FROM endpoint
class from_app(Resource):
    def get(self, yeet):
        # Get most recent document with that yeet name and check if it exists
        document = collection.find_one({"yeet_name": yeet})
        if not (document is None):

            # If it exists, create response and delete document
            response = {"time_created": document["time"], "time_fetched": time.time(), "yeet_name": yeet, "data": document["data"], "success": True}
            collection.delete_one({"yeet_name": yeet})

        else:
            # If it doesn't exist, return a message
            response = {"success": False, "error": "That yeet does not exist, it could have expired or someone could have read it already."}

        return response


api.add_resource(to_app, '/to/<yeet>')
api.add_resource(from_app, '/from/<yeet>')
if __name__ == '__main__':
     app.run(port='8080')
