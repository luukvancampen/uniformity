import csv
import sys
from os import listdir
from os.path import isfile, join
from pathlib import Path
import cchardet as chardet

from column import column
from table import table


def get_file_encoding(path):
    path = Path(path)
    _bytes = path.read_bytes()
    detection = chardet.detect(_bytes)
    return detection["encoding"]


def fix_nulls(s):
    for line in s:
        yield line.replace('\0', '')

def get_csv_rows_fix_null(path):
    csv.field_size_limit(sys.maxsize)
    encoding = get_file_encoding(path)
    rows = []
    with open(path, encoding=encoding) as fd:
        reader = csv.reader(fix_nulls(fd), delimiter=',', quotechar='"')
        for row in reader:
            rows.append(row)
    return rows


def get_tsv_rows_fix_null(path):
    csv.field_size_limit(sys.maxsize)
    encoding = get_file_encoding(path)
    rows = []
    with open(path, encoding=encoding) as fd:
        reader = csv.reader(fix_nulls(fd), delimiter='\t', quotechar='"')
        for row in reader:
            rows.append(row)
    return rows


def parse_csv(_file):
    splitted = _file.split("/")
    filename = splitted[-1].split('.')[0]
    rows = get_csv_rows_fix_null(_file)
    header = rows[0]
    rows.pop(0)

    columns = []
    test_rows = get_csv_rows_fix_null(_file)
    test_rows.pop(0)
    splitted_rows = []
    for r in test_rows:
        try:
            splitted_rows.append(r)
        except IndexError:
            print(_file)
            print(test_rows)
            print(type(test_rows))

    print("Number of rows: ", str(len(splitted_rows)))
    for index, _column in enumerate(header):
        data = []
        for row in splitted_rows:
            try:
                data.append(row[index])
            except IndexError:
                data.append("")
        columns.append(column(_column, data, filename))

    print(table(filename, columns).to_json())

    return table(filename, columns)


# This method return an instance of class "table".
def parse_tsv(_file):
    splitted = _file.split("/")
    filename = splitted[-1].split('.')[0]
    rows = get_csv_rows_fix_null(_file)
    header = rows[0]
    header_string = header[0]
    header = header_string.split('\t')
    rows.pop(0)

    columns = []
    test_rows = get_tsv_rows_fix_null(_file)
    test_rows.pop(0)
    splitted_rows = []
    for r in test_rows:
        try:
            splitted_rows.append(r)
        except IndexError:
            print(_file)
            print(test_rows)
            print(type(test_rows))

    print("Number of rows: ", str(len(splitted_rows)))
    for index, _column in enumerate(header):
        data = []
        for row in splitted_rows:
            try:
                data.append(row[index])
            except IndexError:
                data.append("")
        columns.append(column(_column, data, filename))

    print(table(filename, columns).to_json())

    return table(filename, columns)


def files_to_tables(directory):
    files = [f for f in listdir(directory) if isfile(join(directory, f)) and (f.endswith(".tsv") or f.endswith(".csv"))]
    tables = []
    for file in files:
        if file.endswith(".csv"):
            _table = parse_csv(join(directory, file))
            tables.append(_table)
        elif file.endswith(".tsv"):
            _table = parse_tsv(join(directory, file))
            tables.append(_table)

    return tables
