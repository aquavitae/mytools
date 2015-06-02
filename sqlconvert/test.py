#!/usr/bin/env python3

import difflib
import os.path
import sqlconvert


tests = [
    ('mssql', 'mssql.sql', 'mssql.output.sql'),
]


for fmt, infile, outfile in tests:
    print('Testing {}... '.format(fmt), end='')
    with open(os.path.join('tests', infile), 'r') as fh:
        got = sqlconvert.convert(fh.read(), fmt)
    with open(os.path.join('tests', outfile), 'r') as fh:
        expect = fh.read()

    diff = list(difflib.context_diff(expect.split(), got.split(),
                                     'Expected', 'Got'))
    if diff:
        print('FAIL!')
        print(repr(diff))
        for line in diff:
            print(line)
    else:
        print('PASS')
