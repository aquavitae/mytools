#!/usr/bin/env python3

"""
Convert sql to MYSQL using regular expressions.

Example usage:

    sqlconvert.py mssql.sql --format mssql > mysql_output.sql
"""


import argparse
import re
import sys

regexes = {
    'mssql': [
        [r'\bGO\b', ';'],
        [r'\[numeric\]', 'numeric'],
        [r'\[image\]', 'blob'],
        [r'\[smalldatetime\]', 'datetime'],
        [r'\[decimal\]', 'decimal'],
        [r'\[money\]', 'decimal(12,2)'],
        [r'\[smallmoney\]', 'decimal(12,2)'],
        [r'\[bit\]', 'tinyint'],
        [r'\[smallint\]', 'int'],
        [r'\[float\]', 'double'],
        [r'\[(n?var)?char\]', 'varchar'],
        [r'varchar\(max\)', 'varchar(65535)'],
        [r'\[datetime\]', 'datetime'],
        [r'\[text\]', 'text'],
        [r'\[int\]', 'int'],
        [r' ON \[PRIMARY\]', ''],
        [r' TEXTIMAGE_ON \[PRIMARY\]', ''],
        [r'\[dbo\]\.', ''],
        [r'\[', '`'],
        [r'\]', '`'],
        [r'(CREATE\sDATABASE\s`[^`]*`)[^;]*', r'\1'],
        [r'ALTER\sDATABASE\s`[^`]*`[^;]*;\s', r''],
        [r'(ALTER TABLE `[^`]+` ADD)([^,;]+ FOREIGN KEY [^,;]+),', ''],
        [r'COLLATE [^ ]+.', ''],
        [r'IDENTITY\([^)]+.', 'AUTO_INCREMENT'],
        [r'IDENTITY \([^)]+.', 'AUTO_INCREMENT'],
        [r'WITH \([^)]+.', ''],
        [r'WITH\([^)]+.', ''],
        [r' NOT FOR REPLICATION', ''],
        [r' CLUSTERED', ''],
        [r'SET ANSI_NULLS [^;]*?;', ''],
        [r'SET QUOTED_IDENTIFIER [^;]*?;', ''],
        [r'SET ANSI_PADDING [^;]*?;', ''],
    ]
}


def convert(sql, format):
    replace = regexes[format.lower()]
    for regex, repl in replace:
        sql = re.sub(regex, repl, sql, flags=re.I | re.M)
    return sql


def main():
    parser = argparse.ArgumentParser(
        description="Convert a sql file to mysql format. " +
                    "Valid input formats are MSSQL"
    )
    parser.add_argument('inputfile')
    parser.add_argument('-f', '--format', help='Format to convert from')
    args = parser.parse_args()

    with open(args.inputfile, 'r') as fh:
        print(convert(fh.read(), args.format))


if __name__ == '__main__':
    main()
