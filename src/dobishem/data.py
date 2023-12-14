"""Some generic data operations, mostly for data used with csv.DictReader and csv.DictWriter.."""

import datetime
from dates import as_date

def rename_columns(raw, column_renames):
    """Returns a row dictionary or a header list with columns renamed."""
    return ({column_renames.get(key, key): value for key, value in raw.items()}
            if isinstance(raw, dict)
            else [column_renames.get(key, key) for key in raw])

def transform_cells(row, transformations):
    """Returns a row dict with column-specific transformations applied."""
    return {k: transformations.get(k, lambda a: a)(v)
            for k, v in row.items()}

def matches(row, match_key, match_value):
    """Returns whether a row contains a given value in a given column.
    If no column is given, returns True."""
    return (match_key is None
            or row.get(match_key) == match_value)

def entries_between_dates(incoming, starting, ending):
    "Return the entries in a list that are between two given dates."
    starting = as_date(starting)
    ending = as_date(ending)
    return [entry
            for entry in incoming
            if starting <= as_date(entry['Date']) <= ending]
