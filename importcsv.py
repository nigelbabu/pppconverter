#!/usr/bin/env python
from website import Country, db
import csv
import argparse

def main(file_name):
    with open(file_name) as ppp_data:
        for line in ppp_data:
            country = Country(name=line[0], code3=line[1],
                              year=line[2], ppp=line[3])
            db.session.add(country)
            db.session.commit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Import CSV into the database'
                                     )
    parser.add_argument('-f', '--file', required=True, help='Path to the CSV '
                        'file')
    args = parser.parse_args()
    main(args.file)
