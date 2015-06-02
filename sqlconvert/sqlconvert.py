#!/usr/bin/env python3

"""
Convert sql to MYSQL using regular expressions.

Example usage:

    sqlconvert.py mssql.sql --format mssql > mysql_output.sql
"""


import argparse
import re


# Lists of regular expressions and replacement strings for each sql syntax.
# For each row, the first value is the regex to match and the second in the
# replacement (see `re.sub` for details).  In addition, if the reges contains
# groups named 'match' and 'replace', then the values in those groups are
# also matched and replaced immediately.
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
    ],

    'interbase5': [
        [r'CREATE\sDATABASE\s+"[^"]*\\(\w+)[^"]*?"([^;]*);',
            r'CREATE DATABASE `\1` \2;\nUSE `\1`;'],
        [r'\bPAGE_SIZE\s\d+', r'/* \g<0> */'],
        [r'DECLARE[^;]*?;', r'/* \g<0> */'],
        [r'SET AUTODDL [^;]*?;', r'/* \g<0> */'],
        [r'\bSET TERM\b', r'DELIMITER'],
        [r'CREATE GENERATOR [^;]*?;\s*', r'/* \g<0> */'],
        [r'CREATE EXCEPTION [^;]*?;\s*', r'/* \g<0> */'],
        [r'''["']''', '`'],
        [r'ALTER TABLE `?\w+`?\s+ADD\s+CHECK[^;]*;', r'/* \g<0> */'],
        [r'\bCREATE\sDOMAIN\s(?P<match>\w+)\sAS\s(?P<replace>[^;]*);\s+', r'/* \g<0> */'],
        [r'BLOB (?P<a>(SUB_TYPE \w+\s*)?(SEGMENT SIZE \d+\s*)?(CHARACTER SET \w+)?)\s*(?P<b>[^,]*),',
            r"BLOB \g<b> COMMENT '\g<a>',"],
    ]
}


def replace(regex, repl, sql):
    # Check if the regex contains 'match' and 'replace' groups
    r = r'.*\(\?P<%s>.*?\)'
    extram = []
    if re.search(r % 'match', regex) and re.search(r % 'replace', regex):
        extram = re.findall(regex, sql)
    sql = re.sub(regex, repl, sql, flags=re.I | re.M | re.S)
    for match, repl in extram:
        sql = replace(match, repl, sql)
    return sql


def convert(sql, fmt):
    for regex, repl in regexes[fmt.lower()]:
        sql = replace(regex, repl, sql)
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
        mysql = convert(fh.read(), args.format)
        print(mysql)


if __name__ == '__main__':
    main()
