# import relevant modules
# flask - to set up the server
# os - to get environmental variables
# json - to work with json format
from flask import Flask, request
from flask import jsonify
import os
import json
import uuid

# to allow cors, if else the client would get a cors error
from flask_cors import CORS

# import the connection of the database and all of the functions used inside the routes
# from idg2001_oblig2_api.database import db
from .database import db


# from functions import *
# import idg2001_oblig2_api.converter as converter
# from idg2001_oblig2_api import converter
from . import converter

# to get information from the environmental variable
from dotenv import load_dotenv
load_dotenv()

# Setup the server
app = Flask(__name__)

# allow cors on all of the routes
CORS(app, resources={r"/*": {"origins": ["*"]}})

# set up API Keys from the environmental variable
API_KEY = os.getenv("API_KEY")
print(API_KEY)


# Checks if it is the right key
def check_api_key():

    # Checks if it exists a key variable at all
    if not API_KEY:
        raise ValueError('API_KEY environment variable not set')

    key = request.args.get('key')
    print('dotenv', repr(API_KEY))
    print('key', repr(key))

    if key is None:
        print('API key is missing')
        return 'API key is missing'

    if key != API_KEY:
        print('Invalid API key')
        return 'Invalid API key'
    
    return 

# changes the id to string
def id2str(document, unique_id):
    document["uuid"] = str(unique_id)
    return document


# add contact in database
@app.route("/contacts", methods=["POST"])
def add_to_db_route():
    error = check_api_key()
    if error:
        return jsonify(error)
    print('in post')
    test = request.get_json()
    print('this is with get_json: ', test)
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
        json_contacts = converter.get_all_contacts()
    vcard_contacts = converter.get_all_contacts_vcard()

    # Serialize the dictionaries to JSON strings
    # json_contacts_str = json.dumps(json_contacts)
    # vcard_contacts_str = json.dumps(vcard_contacts)

    # Create a dictionary to hold the JSON responses
    response = {
        "json": json_contacts,
        "vcard": vcard_contacts
    }

    # Use the jsonify function to automatically serialize the dictionary to JSON
    return jsonify(response)


@app.route("/contacts", methods=["GET"])
def get_all_contacts_JSON_route():
    error = check_api_key()
    if error:
        return jsonify(error)
    all_contacts = converter.get_all_contacts()
    return json.loads(all_contacts)


# GET all contacts in vcard format inside a JSON structure
@app.route("/contacts/vcard", methods=["GET"])
def get_all_contacts_vcard_route():
    error = check_api_key()
    if error:
        return jsonify(error)
    all_contacts_vcard = converter.get_all_contacts_vcard()
    return {"message": all_contacts_vcard}


# GET all contacts in JSON format
@app.route("/contacts/<id>", methods=["GET"])
def get_contact_JSON_route(id):
    error = check_api_key()
    if error:
        return jsonify(error)
    return converter.get_contact(id)


# GET contact by id and visualize in vcard format inside a JSON structure
@app.route("/contacts/<id>/vcard", methods=["GET"])
def get_contact_vcard_route(id):
    error = check_api_key()
    if error:
        return jsonify(error)
    contact_vcard = converter.get_contact_vcard(id)
    return {"message": contact_vcard}


if __name__ == "__main__":
    app.run("0.0.0.0", debug=True, port=os.getenv("PORT", default=5000))  # type: ignore
