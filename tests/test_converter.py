import pytest

from idg2001_oblig2_api.converter import split_content

# from converter import process_lines, split_content

# # define a test function that checks the behavior of the function
# def test_process_lines():
#     # create a list of input lines to test the function with
#     lines = [
#         'BEGIN:VCARD\n',
#         'VERSION:3.0\n',
#         'N:Stenerson;Derik\n',
#         'FN:Derik Stenerson\n',
#         'BDAY;VALUE=DATE:1963-09-21\n',
#         'ORG:Microsoft Corporation\n',
#         # 'ADR;TYPE=WORK,POSTAL,PARCEL:;;One Microsoft Way;Redmond;WA;98052-6399;USA\n'
#         # 'TEL;TYPE=WORK,MSG:+1-425-936-5522\n',
#         # 'TEL;TYPE=WORK,FAX:+1-425-936-7329\n',
#         # 'EMAIL;TYPE=INTERNET:deriks@Microsoft.com\n',
#         'END:VCARD\n'
#     ]

#     # define the pattern to match
#     pattern = r'^N:'

#     # call the function with the test inputs
#     result = process_lines(lines, pattern)

#     # define the expected output
#     expected_output = {
#         # 'version:3.0\n',
#         'name:Stenerson;Derik\n',
#         'full_name:Derik Stenerson\n',
#         'birthday:1963-09-21\n',
#         'organisation:Microsoft Corporation\n',
#         # 'address_WORK: [{prefix: ,POSTAL,PARCEL:;;,value: One Microsoft Way;Redmond;WA;98052-6399;USA}]\n'
#         # 'telephone;TYPE=WORK,MSG:+1-425-936-5522\n',
#         # 'telephone;TYPE=WORK,FAX:+1-425-936-7329\n',
#         # 'email;TYPE=INTERNET:deriks@Microsoft.com\n',
#     }

#     # check that the actual output matches the expected output
#     assert result == expected_output

def test_split_content():
    content = "BEGIN:VCARD\nName:John\nEND:VCARD\nBEGIN:VCARD\nName:Jane\nEND:VCARD\n"
    result = split_content(content)
    expected_output = ["BEGIN:VCARD\nName:John\n", "\nBEGIN:VCARD\nName:Jane\n", "\n"]
    assert result == expected_output