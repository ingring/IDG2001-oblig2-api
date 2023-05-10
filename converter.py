from flask import Flask, request, jsonify
import os
import json
import re
from database import db

from bson import ObjectId
from bson.json_util import dumps, loads


# Replace the common vcard key's to more human language
# If key is not in this table below, return the key name instead
# Inspired by lab 3
def replace_common_keys(key):
    key_main = key.split(';')[0]
    return {
        'VERSION': 'version',
        'N': 'name',
        'FN': 'full_name',
        'ORG': 'organisation',
        'EMAIL': 'email',
        'BDAY': 'birthday'
    }.get(key_main, key)

# reverts it back to vcard format
def revert_common_keys(key):
    key_main = key.split(';')[0]
    return {
        'version': 'VERSION',
        'name': 'N',
        'full_name': 'FN',
        'organisation': 'ORG',
        'email': 'EMAIL',
        'birthday': 'BDAY'
    }.get(key_main.lower(), key)

# Splits into lists on 'END:VCARD'
def split_content(content):
    return content.split('END:VCARD')

# Removes the last line which is END:VCARD
def remove_last_line(contact_split):
    contact_split[-1] = contact_split[-1].replace('END:VCARD', '')
    return contact_split

# processes each line in the list based on whether it matches the pattern or not
# adds the resulting key-value pairs to a dictionary
def process_lines(lines, pattern):
    contact = {}

    # loops through each line in contact lines 
    for line in lines:
        line = line.strip()

        # remove BEGIN:VCARD
        if line.startswith('BEGIN:'):
            continue

        # remove empty lines
        if len(line) < 1:
            continue

        # if it matches the pattern, use the copy prefix function
        elif re.match(pattern, line):
            line = copy_prefix(line)
            contact.update(line)

        # if not, make a key value pair with the more common human language keys
        else:
            key, *value = line.split(':', 1)
            value = ':'.join(value)
            key = replace_common_keys(key)
            contact[key] = value
    return contact

# since the front end do minimal with the file before sending it to the backend,
# we have to structure the content before we send it to a database
# Inspired by lab 3
def structure_input_text(content):
    # Define the regular expression pattern to match
    pattern = r'^(TEL|ADR).*'

    # splits the vcard content into each contacts
    contact_split = split_content(content)

    # removes the last line in each contact which is END:VCARD
    contact_split = remove_last_line(contact_split)

    # empty list that will hold all of the contacts
    contacts = []

    # loops through each contact and makes a contact object 
    for each_contact in contact_split:
        lines = each_contact.split('\r\n')

        # processes each line in the list of lines based on matching the pattern or not
        # also returns key value pair
        contact = process_lines(lines, pattern)

        # appends the contact object to the contacts list
        contacts.append(contact)
    return contacts
    
# replaces the string, if it matches "TEL" or "ADR" with phone or address
def replace_prefix(str):
    # Define the regular expression pattern to match
    pattern = r'^(TEL|ADR).*'
    pattern_phone = r'^TEL.*'
    pattern_address = r'^ADR.*'

    # If the str matches, replace "TEL" with "phone"
    if re.match(pattern_phone, str):
        return str.replace('TEL', 'phone')

    # If the str matches, replace "ADR" with "address"
    if re.match(pattern_address, str):
        return str.replace('ADR', 'address')

    return str

# replaces semicolons with underscores, if no type is present in the string
def add_type(str):
    # Use regular expressions to extract the type (if present)
    match = re.search(r';TYPE=([^,:;]+)', str)
    if match:
        type_str = match.group(1)

        # Replace semicolons with percent signs to create a URL-friendly string
        type_str = type_str.replace(';', '%', 1)

        # Add the type to the output string
        return str.replace(';TYPE=' + type_str, '_' + type_str + '$')
    else:
        return str.replace(';', '_')


def copy_prefix(str):
    # Replaces "TEL" or "ADR"
    replace_prefix(str)

    # Add the type
    add_type(str)

    # Define the regular expression pattern to match
    pattern = r'^(TEL|ADR).*'

    # Check if the input string matches the regular expression
    if re.match(pattern, str):
        # Replace the prefix
        output_str = replace_prefix(str)

        # Add the type
        output_str = add_type(output_str)

        # reformat and restructure into a dict
        dict = create_dictionary(output_str)
        return dict
    else:
        return str


# creates a dictionary from the string, that includes prefix and value
def create_dictionary(string):
    # if it is a TEL, use these to split the string
    if string.startswith('phone'):
        delimiter = ':+'
        prefix_delimiter = '$'
        default_prefix = ':+'

    # if it is a ADR, use these
    elif string.startswith('address'):
        delimiter = ':;;'
        prefix_delimiter = '$'
        default_prefix = ':;;'

    else:
        raise ValueError('Invalid input string')

    # split the string
    key_prefix, *value = string.split(delimiter)
    key, prefix = key_prefix.split(prefix_delimiter)

    # if there is no prefix on the item, use the default ones.
    # this way it will return the same after converting back to vcf
    prefix = prefix + delimiter if prefix else default_prefix

    if not value:
        value = prefix
        prefix = default_prefix

    value = f"{value}"
    if value.startswith("['") and value.endswith("']"):
        value = value[2:-2]

    # creating the structure we use on the db
    data = {
        key: [{
            "prefix": prefix,
            "value": value
        }]
    }

    return data


# Get all contacts from database
def get_all_contacts():
    result = db['contacts'].find({})
    result = list(result)
    result = dumps(result)
    return json.loads(result)

# get contact by id
def get_contact(id):
    result = db['contacts'].find_one({"_id": ObjectId(id)}, {"_id": 0})
    return result


# format the data from JSON to vCard
def all_vcard_formatter(list_of_contacts):
    pattern = r'^(phone|address).*'

    # Convert the JSON string to a Python dict
    list_of_contacts = loads(list_of_contacts)
    string = ''
    for contact in list_of_contacts:
        string += 'BEGIN:VCARD'
        for item in contact.items():

            # don't include the mongodb id in the vcf
            if item[0] == '_id':
                continue

            # don't include the uuid created column in the vcf
            if item[0] == 'uuid':
                continue

            # if it is a phone or address:
            elif re.match(pattern, item[0]):
                # Replace with the function that creates vCard string
                newString = create_vcard_string(item)
                string += newString
            else:
                # returns the keys in vcard format
                formatted_key = revert_common_keys(item[0])

                # creates the vcard line
                string += '\n' + formatted_key + ':' + item[1]
        string += '\nEND:VCARD\n'
    return string


def one_vcard_formatter(dict):
    pattern = r'^(phone|address).*'

    string = ''
    string += 'BEGIN:VCARD'

    for item in dict.items():
        # don't include the mongodb id in the vcf
        if item[0] == '_id':
            continue

        # don't include the uuid created column in the vcf
        if item[0] == 'uuid':
            continue

        # if it is a phone or address:
        elif re.match(pattern, item[0]):
            # Replace with the function that creates vCard string
            newString = create_vcard_string(item)
            string += newString
        
        else:
            # returns the keys in vcard format
            formatted_key = revert_common_keys(item[0])

            # creates the vcard line
            string += '\n' + formatted_key + ':' + item[1]

    string += '\nEND:VCARD\n'
    return string


def revert_prefix(str):
    # Define the regular expression pattern to match
    pattern_phone = r'^phone.*'
    pattern_address = r'^address.*'

    # Check if the input string matches the regular expression
    if re.match(pattern_phone, str):
        # If the str matches, replace "phone" with "TEL"
        output_str = str.replace('phone', 'TEL')

        # Use regular expressions to extract the type (if present)
        match = re.search(r'_([^$,]+)\$', str)
        if match:
            type_str = match.group(1)

            # Replace percent signs with semicolons to revert the URL-friendly string
            type_str = type_str.replace('%', ';', 1)

            # Add the type to the output string
            output_str = output_str.replace(
                '_' + type_str + '$', ';TYPE=' + type_str)
        else:
            output_str = output_str.replace('_', ';')

    elif re.match(pattern_address, str):
        # If the str matches, replace "address" with "ADR"
        output_str = str.replace('address', 'ADR')

        # Use regular expressions to extract the type (if present)
        match = re.search(r'_([^$,]+)\$', str)
        if match:
            type_str = match.group(1)

            # Replace percent signs with semicolons to revert the URL-friendly string
            type_str = type_str.replace('%', ';', 1)

            # Add the type to the output string
            output_str = output_str.replace(
                '_' + type_str + '$', ';TYPE=' + type_str)
        else:
            output_str = output_str.replace('_', ';')

    else:
        # If the string doesn't match, print an error message
        output_str = str

    # Print the output string
    return output_str


def create_vcard_string(data):
    # save the different elements of the item
    dict = {data[0]: data[1]}
    key = list(dict.keys())[0]
    prefix = dict[key][0]["prefix"]
    value = f"{dict[key][0]['value']}"

    # remove unwanted characters
    if value.startswith("['") and value.endswith("']"):
        value = value[2:-2]
    string = ''

    if key.startswith('phone_'):
        key = key[6:]
        string += 'TEL;TYPE='

    elif key.startswith('address_'):
        key = key[8:]
        string += 'ADR;TYPE='
        # return the item as a string
        
    return f"\n{string}{key}{prefix}{value}"
