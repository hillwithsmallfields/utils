from collections import defaultdict
from frozendict import frozendict
import os
import dobishem.storage

REFERENCE = [ {'Date': "2023-12-09", 'Item': "akullore", 'Price': "1.00"},
              {'Date': "2023-12-09", 'Item': "buke", 'Price': "2.20"},
              {'Date': "2023-12-10", 'Item': "spinaq", 'Price': ".50"},
             ]

REFERENCE_AS_SET = defaultdict(set)
for row in REFERENCE:
    REFERENCE_AS_SET[row['Date']].add(frozendict(row))

def xrow(row):
    return ({'Date': row['Date'],
            'Item': row['Item'],
            'Price': str(1.1 * float(row['Price']))}
            if row['Item'] != "akullore"
            else None)

FILTERED_REFERENCE = [
    xrow(row)
    for row in REFERENCE
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

def test_csv_set(tmp_path):
    filename = os.path.join(tmp_path, "bar.csv")
    dobishem.storage.default_write_csv(filename, REFERENCE)
    assert dobishem.storage.read_csv(filename,
                                     key_column='Date',
                                     result_type=set) == REFERENCE_AS_SET

def test_filtered_csv(tmp_path):
    filename = os.path.join(tmp_path, "baz.csv")
    dobishem.storage.default_write_csv(filename, REFERENCE)
    assert dobishem.storage.read_csv(filename,
                                     key_column='Date',
                                     transform_row=lambda row: xrow)
