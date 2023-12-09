# John Sturdy's storage utils

"""Utility functions for reading and writing files.

The writer functions return what they have written,
so can be used in a passthrough manner."""

from collections import defaultdict
import csv
import json
import os
import yaml

def expand(filename):
    return os.path.expandvars(os.path.expanduser(filename))

def open_for_read(filename, *args, **kwargs):
    return open(expand(filename), *args, **kwargs)

def open_for_write(filename, *args, **kwargs):
    full_name = expand(filename)
    os.makedirs(os.path.dirname(full_name), exists_ok=True)
    return open(expand(filename), 'w', *args, **kwargs)

def read_csv(
        filename,
        result_type=list,
        row_type=list,
        key_column=None,
):
    """Read a CSV file, returning a structure according to result_type.
    The result types are:
    list: a list of rows (key column is ignored)
    dict: a dictionary of rows, keyed by the key column
    set: a dictionary of sets of rows, keyed by the key column

    The elements of the structure are tuples, lists or dicts,
    according to row_type.
    """
    with open_for_read(filename) as instream:
        rows = list(csv.DictReader(instream)
                    if isinstance(row_type, dict)
                    else (tuple(row) for row in csv.reader(instream))
                    if isinstance(row_type, tuple)
                    else csv.reader(instream))
        if isinstance(result_type, set):
            result = defaultdict
            for row in rows:
                result[row[key_column]].append(row)
            return result
        return ({row[key_column]: row
                 for row in rows}
                if isinstance(result, dict)
                else rows)

def default_read_csv(filename):
    return read_csv(filename, result_type=set, row_type=dict, key_column='Date')

def write_csv(
        filename,
        data,
        flatten=False,
        sort_column=None
):
    """Write a CSV file from a list or dict of lists or dicts,
    or, if flatten is true, a dict or list of collections
    of dicts or lists."""
    rows_or_groups = (data.values()
                      if isinstance(data, dict)
                      else data)
    rows = (operator.add([],
                         *(list(row) for row in rows_or_groups))
            if flatten
            else rows_or_groups)
    headers = (
               else None)
    if sort_column:
        rows = sorted(rows, key=lambda row: row[sort_column])
    with open_for_write(filename) as outstream:
        rows_are_dicts = isinstance(rows[0], dict)
        writer = (csv.DictWriter(fieldnames=([sort_column]
                                             + sorted(
                                                 (set().union(*(set(row.keys())
                                                                for row in rows)))
                                                 - set(sort_column))))
                  if rows_are_dicts
                  else csv.writer())
        if rows_are_dicts:
            writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return data

def default_write_csv(filename, data):
    return write_csv(filename, data, flatten=True, sort_column="Date")

def read_json(filename):
    with open_for_read(filename) as instream:
        return json.load(instream)

def write_json(filename, data):
    with open_for_read(filename, 'w') as outstream:
        json.dump(outstream)
    return data

def read_yaml(filename):
    with open_for_read(filename) as instream:
        return yaml.safeload(instream)

def write_yaml(filename, data):
    with open_for_read(filename, 'w') as outstream:
        yaml.dump(outstream)
    return data

READERS = {
    "csv": default_read_csv,
    "json": read_json,
    "yaml": read_yaml,
    }

WRITERS = {
    "csv": default_write_csv,
    "json": write_json,
    "yaml": write_yaml,
    }

def load(filename):
    return READERS[os.path.splitext(filename)](filename)

def save(filename, data):
    return WRITERS[os.path.splitext(filename)](filename, data)
