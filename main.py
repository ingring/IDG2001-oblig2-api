# import relevant modules
# flask - to set up the server
# os - to get environmental variables
# json - to work with json format
from flask import Flask, request
import os
import json

import uuid

import requests

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

API_KEY = os.getenv('API_KEY')

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
def get_all_contacts_JSON_verified():
    provided_api_key = request.headers.get('API-Key')

    if provided_api_key == API_KEY:
        return get_all_contacts()
    else:
        return {'message': 'Invalid API key'}, 401



# GET all contacts in vcard format inside a JSON structure
@app.route('/contacts/vcard', methods=['GET'])
def get_all_contacts_vcard():
    all_contacts = get_all_contacts()
    data = all_vcard_formatter(all_contacts)
    return {"message": data}


# GET all contacts in JSON format
@app.route('/contacts/<id>', methods=['GET'])
def get_contact_JSON(id):
    # return get_contact(id)
    url = f'https://idg2001-oblig2-api.onrender.com/contacts/{id}'
    headers = {'Authorization': f'Bearer {API_KEY}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return 'Error: Unable to retrieve contact', response.status_code


# GET contact by id and visualize in vcard format inside a JSON structure
@app.route('/contacts/<id>/vcard', methods=['GET'])
def get_contact_vcard(id):
    contact = get_contact(id)
    data = one_vcard_formatter(contact)
    return {"message": data}


if __name__ == '__main__':
    app.run("0.0.0.0", debug=True, port=os.getenv("PORT", default=5000))
