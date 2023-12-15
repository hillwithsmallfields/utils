"""Some generic data operations, mostly for data used with csv.DictReader and csv.DictWriter.."""

import datetime

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
