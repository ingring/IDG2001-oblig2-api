from idg2001_oblig2_api.__main__ import id2str


# testes to make the id to string, also test when it is a empty dict
def test_id2str():
    assert id2str({"uuid": 123}, 456) == {"uuid": "456"}
    assert id2str({}, 789) == {"uuid": "789"}
