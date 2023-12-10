import os
import dobishem.storage

REFERENCE = [ {'Date': "2023-12-09", 'Item': "akullore", 'Price': "1.00"},
              {'Date': "2023-12-09", 'Item': "buke", 'Price': "2.20"},
              {'Date': "2023-12-10", 'Item': "spinaq", 'Price': ".50"},
             ]

def test_csv(tmp_path):
    filename = os.path.join(tmp_path, "foo.csv")
    dobishem.storage.default_write_csv(filename, REFERENCE)
    assert dobishem.storage.default_read_csv(filename) == REFERENCE

def test_json(tmp_path):
    filename = os.path.join(tmp_path, "foo.json")
    dobishem.storage.write_json(filename, REFERENCE)
    assert dobishem.storage.read_json(filename) == REFERENCE

def test_yaml(tmp_path):
    filename = os.path.join(tmp_path, "foo.yaml")
    dobishem.storage.write_yaml(filename, REFERENCE)
    assert dobishem.storage.read_yaml(filename) == REFERENCE

def test_generic(tmp_path):
    for extension in ["csv", "json", "yaml"]:
        filename = os.path.join(tmp_path, "foo." + extension)
        dobishem.storage.save(filename, REFERENCE)
        assert dobishem.storage.load(filename) == REFERENCE
