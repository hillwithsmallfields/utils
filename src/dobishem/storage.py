# John Sturdy's storage utils

"""Utility functions for reading and writing files.

The writer functions return what they have written,
so can be used in a passthrough manner.

All the functions using filenames expand environment variables and '~'
in the names.
"""

from collections import defaultdict
import csv
import glob
import json
import os
import yaml

def _expand(filename):
    """Expand environment variables and '`~' in a filename."""
    return os.path.expandvars(os.path.expanduser(filename))

def open_for_read(filename, *args, **kwargs):
    """Return an input stream for the named file."""
    return open(_expand(filename), *args, **kwargs)

def open_for_write(filename, *args, **kwargs):
    """Return an output stream to the named file.
    If necessary, create the directory the file is to go into."""
    full_name = _expand(filename)
    os.makedirs(os.path.dirname(full_name), exist_ok=True)
    return open(full_name, 'w', *args, **kwargs)

def read_csv(
        filename,
        result_type=list,
        row_type=dict,
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
                    if issubclass(row_type, dict)
                    else ((tuple(row) for row in csv.reader(instream))
                          if issubclass(row_type, tuple)
                          else csv.reader(instream)))
        if issubclass(result_type, set):
            result = defaultdict()
            for row in rows:
                result[row[key_column]].append(row)
            return result
        return ({row[key_column]: row
                 for row in rows}
                if issubclass(result_type, dict)
                else rows)

def default_read_csv(filename):
    """Read a CSV file as for a list of dated entries."""
    return read_csv(filename, key_column='Date')

def write_csv(
        filename,
        data,
        flatten=False,
        sort_columns=[]
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
    if sort_columns:
        rows = sorted(rows, key=lambda row: [row[k] for k in sort_columns])
    with open_for_write(filename) as outstream:
        rows_are_dicts = isinstance(rows[0], dict)
        writer = (csv.DictWriter(outstream,
                                 fieldnames=(sort_columns
                                             + sorted(
                                                 (set().union(*(set(row.keys())
                                                                for row in rows)))
                                                 - set(sort_columns))))
                  if rows_are_dicts
                  else csv.writer(outstream))
        if rows_are_dicts:
            writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return data

def default_write_csv(filename, data):
    """Write a CSV file as for a list of dated entries."""
    return write_csv(filename, data, sort_columns=["Date", "Item"])

def read_json(filename):
    """Read a JSON file."""
    with open_for_read(filename) as instream:
        return json.load(instream)

def write_json(filename, data):
    """Write a JSON file."""
    with open_for_read(filename, 'w') as outstream:
        json.dump(data, outstream)
    return data

def read_yaml(filename):
    """Read a YAML file."""
    with open_for_read(filename) as instream:
        return yaml.safe_load(instream)

def write_yaml(filename, data):
    """Write a YAML file."""
    with open_for_read(filename, 'w') as outstream:
        yaml.dump(data, outstream)
    return data

READERS = {
    ".csv": default_read_csv,
    ".json": read_json,
    ".yaml": read_yaml,
    }

WRITERS = {
    ".csv": default_write_csv,
    ".json": write_json,
    ".yaml": write_yaml,
    }

def load(filename):
    """Read a file, finding a suitable reader function for the filename."""
    return READERS[os.path.splitext(filename)[1]](filename)

def save(filename, data):
    """Write a file, finding a suitable writer function for the filename."""
    return WRITERS[os.path.splitext(filename)[1]](filename, data)

def function_cached_with_file(function, filename):
    """Read a file and return its contents.
    If the file does not exist, run a function to create the contents,
    write them to the file, and return them."""
    filename = _expand(filename)
    return (load(filename)
            if os.path.exists(filename)
            else save(filename, function()))

def modified(filename):
    """Return the modification time of a file."""
    return os.path.getmtime(_expand(filename))

def file_newer_than_file(a, b):
    return os.path.getmtime(_expand(a)) > os.path.getmtime(_expand(b))

def in_modification_order(filenames):
    """"Return a list of filenames sorted into modification order.
    If the filenames are given as a string rather than a list,
    apply shell-style globbing to convert it to a list."""
    if isinstance(filenames, str):
        filenames = glob.glob(_expand(filenames))
    return sorted(filenames, key=modified)

def most_recently_modified(filenames):
    """Return the most recently modified of a list of files."""
    return in_modification_order(filenames)[-1]

def combined(destination, combiner, origins):
    """If any of the origin files have been updated since the destination
    was, run the combiner function on their contents and write its
    result to the destination, returning the result.

    The 'combiner' argument is a function taking a list of lists,
    typically, the result of reading multiple CSV files, and its
    result would typically be a list to be written to a CSV file.

    The 'origins' argument is a dictionary binding filename strings to
    row processing functions, so this function can be used to
    transform incoming data and merge it into a collection.  If a row
    processing function returns `None`, the row is skipped.

    Otherwise, read and return the destination file.
    """
    return (save(destination,
                 combiner([[entry
                            for raw in load(origin)
                            if (entry := converter(raw)) is not None]
                           for origin, converter in origins.items()]))
            if (modified(destination)
                < modified(most_recently_modified(origins)))
            else load(destination))
