# import relevant modules
# flask - to set up the server
# os - to get environmental variables
# json - to work with json format
from flask import Flask, request
import os
import json

import uuid

# import the connection of the database and all of the functions used inside the routes
# from idg2001_oblig2_api.database import db
# from .database import db
from idg2001_oblig2_api.database import db


# from functions import *
# import idg2001_oblig2_api.converter as converter
# from . import converter
from idg2001_oblig2_api import converter

from dotenv import load_dotenv
import requests

load_dotenv()

# to allow cors, if else the client would get a cors error
from flask_cors import CORS

API_KEY = os.getenv("API_KEY")
print(API_KEY)
if not API_KEY:
    raise ValueError('API_KEY environment variable not set')

# Setup the server
app = Flask(__name__)

# allow cors on all of the routes
CORS(app, resources={r"/*": {"origins": ["*"]}})


def id2str(document, unique_id):
    document["uuid"] = str(unique_id)
    return document


# add contact in database
@app.route("/contacts", methods=["POST"])
def add_to_db_route():
    data = request.json["message"]  # type: ignore
    contact_list = converter.structure_input_text(data)
    for document in contact_list:
        if document:
            # uses uuid to set a unique id to prevent duplicate documents in the same post request
            unique_id = uuid.uuid4()
            document = id2str(document, unique_id)
            db["contacts"].update_one(
                {"uuid": document["uuid"]}, {"$set": document}, upsert=True
            )
    contact = json.dumps(contact_list)
    return Flask.jsonify({"message": contact})  # type: ignore


# GET all contacts in JSON format
@app.route("/contacts", methods=["GET"])
def get_all_contacts_JSON_route():
    all_contacts = converter.get_all_contacts()
    key = request.args.get('key')
    print('dotenv', repr(API_KEY))
    print('key', repr(key))
    if key is None:
        print('API key is missing')
        return {'message': 'API key is missing'}, 401
    if key != API_KEY:
        print('Invalid API key')
        return {'message': 'Invalid API key'}, 401
    # if provided_key == API_KEY:
        # all_contacts = list(all_contacts)
        # all_contacts = dumps(all_contacts)
    return json.loads(all_contacts)


# GET all contacts in vcard format inside a JSON structure
@app.route("/contacts/vcard", methods=["GET"])
def get_all_contacts_vcard_route():
    all_contacts_vcard = converter.get_all_contacts_vcard()
    key = request.args.get('key')
    print('dotenv', repr(API_KEY))
    print('key', repr(key))
    if key is None:
        print('API key is missing')
        return {'message': 'API key is missing'}, 401
    if key != API_KEY:
        print('Invalid API key')
        return {'message': 'Invalid API key'}, 401
    return {"message": all_contacts_vcard}


# GET all contacts in JSON format
@app.route("/contacts/<id>", methods=["GET"])
def get_contact_JSON_route(id):
    key = request.args.get('key')
    print('dotenv', repr(API_KEY))
    print('key', repr(key))
    if key is None:
        print('API key is missing')
        return {'message': 'API key is missing'}, 401
    if key != API_KEY:
        print('Invalid API key')
        return {'message': 'Invalid API key'}, 401
    return converter.get_contact(id)


# GET contact by id and visualize in vcard format inside a JSON structure
@app.route("/contacts/<id>/vcard", methods=["GET"])
def get_contact_vcard_route(id):
    key = request.args.get('key')
    print('dotenv', repr(API_KEY))
    print('key', repr(key))
    if key is None:
        print('API key is missing')
        return {'message': 'API key is missing'}, 401
    if key != API_KEY:
        print('Invalid API key')
        return {'message': 'Invalid API key'}, 401
    contact_vcard = converter.get_contact_vcard(id)
    return {"message": contact_vcard}


if __name__ == "__main__":
    app.run("0.0.0.0", debug=True, port=os.getenv("PORT", default=5000))  # type: ignore
