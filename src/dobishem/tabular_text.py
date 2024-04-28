# Read and write org-mode style tables

import re

DIVIDER = re.compile(r"^ *\|[-+]+\| *$")

def cells(line):
    return [cell.strip() for cell in line.strip().split("|")[1:-1]]

def is_divider(line):
    return DIVIDER.match(line)

def is_layout(line):
    return (not line
            or is_divider(line))

def read_tabular_to_lists(source):
    """Read tabular text to lists of cells."""
    return (cells(line)
            for line in source
            if not is_layout(line))

def read_tabular_to_dicts(source):
    """Read a tabular text to a list dicts of cells, and a column order list."""
    rows = read_tabular_to_lists(source)
    header = next(rows)
    return ({k: v for k, v in dict(zip(header, row)).items() if v}
            for row in rows), header

def dicts_to_tabular_string(data, column_order=[]):
    """Convert a list of dicts to a tabular string."""
    as_strings = [{name: str(cell) for name, cell in row.items()} for row in data]
    all_columns = column_order + sorted(set().union(*[set(record.keys())
                                                      for record in as_strings])
                                        - set(column_order))
    widths = {name: max(len(name),
                        max(len(row.get(name, "")) for row in as_strings))
              for name in all_columns}
    hline = "|-" + "-+-".join("-" * widths[colname] for colname in all_columns) + "-|"
    formats = {colname: "%%-%ds" % colwidth
               for colname, colwidth in widths.items()}
    return "\n".join([hline,
                      "| " + " | ".join([formats[colname] % colname for colname in all_columns]) + " |",
                      hline]
                     + ["| " + " | ".join([formats[colname] % row.get(colname, "") for colname in all_columns]) + " |"
                        for row in as_strings]
                     + [hline])

def write_tabular(stream, data, column_order=[]):
    """Write tabular data to a stream."""
    stream.write(dicts_to_tabular_string(data, column_order))
    return data
