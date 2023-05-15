from idg2001_oblig2_api.converter import split_content, remove_last_line


# tests if it splits the vcard text
def test_split_content():
    content = "BEGIN:VCARD\nName:John\nEND:VCARD\nBEGIN:VCARD\nName:Jane\nEND:VCARD\n"
    result = split_content(content)
    expected_output = ["BEGIN:VCARD\nName:John\n", "\nBEGIN:VCARD\nName:Jane\n", "\n"]
    assert result == expected_output


# tests if it removes the last line at the vcard text
def test_remove_last_line():
    contact_split = ['BEGIN:VCARD\n', 'VERSION:3.0\n', 'N:Doe;John;;;\n', 'FN:John Doe\n', 'END:VCARD']
    expected_result = ['BEGIN:VCARD\n', 'VERSION:3.0\n', 'N:Doe;John;;;\n', 'FN:John Doe\n', '']
    assert remove_last_line(contact_split) == expected_result