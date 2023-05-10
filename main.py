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
def add_to_db():
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
def get_all_contacts_JSON():
    return get_all_contacts()


# GET all contacts in vcard format inside a JSON structure
@app.route('/contacts/vcard', methods=['GET'])
def get_all_contacts_vcard():
    all_contacts = get_all_contacts()
    data = all_vcard_formatter(all_contacts)
    return {data}


# GET all contacts in JSON format
@app.route('/contacts/<id>', methods=['GET'])
def get_contact_JSON(id):
    return get_contact(id)


# GET contact by id and visualize in vcard format inside a JSON structure
@app.route('/contacts/<id>/vcard', methods=['GET'])
def get_contact_vcard(id):
    contact = get_contact(id)
    data = one_vcard_formatter(contact)
    return {"message":data}


if __name__ == '__main__':
    app.run("0.0.0.0", debug=True, port=os.getenv("PORT", default=5000))
