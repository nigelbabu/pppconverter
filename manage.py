#!/usr/bin/env python
import argparse
import csv
import codecs
import json
import requests
from flask.ext.script import Manager
from website import Country, Config, db, app

manager = Manager(app)

@manager.option('-f', '--file_name', required=True, help='Path to the CSV file')
def importcountries(file_name):
    '''Import the countries CSV into the database'''
    with open(file_name) as f:
        country_data = csv.reader(f)
        for line in country_data:
            country = Country.query.filter_by(code3=line[3]).first()
            if country:
                country.currency = line[14]
                db.session.add(country)
                db.session.commit()
    print("Imported CSV successfully")


@manager.option('-f', '--file_name', required=True, help='Path to the CSV file')
def importcsv(file_name):
    '''Import a CSV into the database'''
    with open(file_name) as f:
        ppp_data = csv.reader(f)
        for line in ppp_data:
            country = Country(name=line[0], code3=line[1],
                              year=line[2], ppp=line[3])
            db.session.add(country)
            db.session.commit()
    print("Imported CSV successfully")


@manager.option('-f', '--file_name', required=True, help='Path to the CSV file')
def parsecsv(file_name = None):
    '''Parse a CSV file from the World Bank'''

    def extract_values(data):
        list_of_years = ['2014', '2013', '2012', '2011', '2010', '2009',
                '2008', '2007', '2006', '2005', '2004', '2003', '2002', '2001',
                '2000', '1999', '1998', '1997', '1996', '1995', '1994', '1993',
                '1992', '1991', '1990', '1989', '1988', '1987', '1986', '1985',
                '1984', '1983', '1982', '1981', '1980', '1979', '1978', '1977',
                '1976', '1975', '1974', '1973', '1972', '1971', '1970', '1969',
                '1968', '1967', '1966', '1965', '1964', '1963', '1962', '1961',
                '1960']

        for year in list_of_years:
            if data.get(year):
                    return year, data.get(year)
        return None, None

    new_csv = []
    # The CSV file from world bank as a UTF-8 BOM necessating the following
    # code.
    with codecs.open(file_name, 'r', 'utf-8-sig') as csvfile:
        data_dict = csv.DictReader(csvfile)
        for row in data_dict:
            new_row = {}
            year, value = extract_values(row)
            if year is None or value is None:
                continue
            new_row = {'year': year, 'value': value, 'country':
                       row['Country Name'], 'code': row['Country Code']}
            new_csv.append(new_row)
    with open('parsed_data.csv', 'w') as csvfile:
        dict_writer = csv.DictWriter(csvfile, ['country', 'code', 'year',
                                     'value'])
        dict_writer.writerows(new_csv)
    print("Parsed CSV successfully")


@manager.command
def update_conversion_rate():
    '''Update the converstion rate from openexchangerate'''
    params = {'app_id': app.config['OPEN_EXCHANGE']}
    try:
        r = requests.get('http://openexchangerates.org/api/latest.json',
                         params=params)
    except requests.exceptions.ConnectionError:
        return "Couldn't connect to the server"
    except requests.exceptions.HTTPError:
        return "The server returned an error"
    response_dict = r.json()
    rates = response_dict.get('rates', {})
    gbp_rate = rates.get('GBP')
    db_entry = Config.query.filter_by(key='gbp_rate').first()
    if db_entry:
        db_entry.value = gbp_rate
    else:
        db_entry = Config(key='gbp_rate', value=gbp_rate)
    db.session.add(db_entry)
    db.session.commit()
    print("Updated conversion rate")


@manager.command
def db_init():
    db.create_all()


if __name__ == '__main__':
    manager.run()
