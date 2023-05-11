# import relevant modules
# flask - to set up the server
# os - to get environmental variables
# json - to work with json format
from flask import Flask, request
import os
import json

import uuid

# import the connection of the database and all of the functions used inside the routes
from database import db
# from functions import *
from converter import *

# to allow cors, if else the client would get a cors error
from flask_cors import CORS, cross_origin

# Setup the server
app = Flask(__name__)

# allow cors on all of the routes
CORS(app, resources={
     r"/*": {"origins": ["*"]}})

# add contact in database
@app.route('/contacts', methods=['POST'])
def add_to_db_route():
    data = request.json['message']
    contact_list = structure_input_text(data)
    for document in contact_list:
        if document:
            # uses uuid to set a unique id to prevent duplicate documents in the same post request
            document['uuid'] = str(uuid.uuid4())
            db['contacts'].update_one({'uuid': document['uuid']}, {
                                      '$set': document}, upsert=True)
    contact = json.dumps(contact_list)
    return jsonify({"message": contact})


# GET all contacts in JSON format
@app.route('/contacts', methods=['GET'])
def get_all_contacts_JSON_route():
    all_contacts = get_all_contacts()
    # all_contacts = list(all_contacts)
    # all_contacts = dumps(all_contacts)
    return json.loads(all_contacts)


# GET all contacts in vcard format inside a JSON structure
@app.route('/contacts/vcard', methods=['GET'])
def get_all_contacts_vcard_route():
    all_contacts_vcard = get_all_contacts_vcard()
    return {"message":all_contacts_vcard}


# GET all contacts in JSON format
@app.route('/contacts/<id>', methods=['GET'])
def get_contact_JSON_route(id):
    return get_contact(id)


# GET contact by id and visualize in vcard format inside a JSON structure
@app.route('/contacts/<id>/vcard', methods=['GET'])
def get_contact_vcard_route(id):
    contact_vcard = get_contact_vcard(id)
    return {"message":contact_vcard}


if __name__ == '__main__':
    app.run("0.0.0.0", debug=True, port=os.getenv("PORT", default=5000))
