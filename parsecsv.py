#!/usr/bin/env python
import csv
import codecs


def main():
    new_csv = []
    # The CSV file from world bank as a UTF-8 BOM necessating the following
    # code.
    with codecs.open('new_data.csv', 'r', 'utf-8-sig') as csvfile:
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
        dict_writer = csv.DictWriter(csvfile, ['year', 'value', 'country',
                                     'code'])
        dict_writer.writerows(new_csv)



def extract_values(data):
    list_of_years = ['2013', '2012', '2011', '2010', '2009', '2008', '2007',
            '2006', '2005', '2004', '2003', '2002', '2001', '2000', '1999',
            '1998', '1997', '1996', '1995', '1994', '1993', '1992', '1991',
            '1990', '1989', '1988', '1987', '1986', '1985', '1984', '1983',
            '1982', '1981', '1980', '1979', '1978', '1977', '1976', '1975',
            '1974', '1973', '1972', '1971', '1970', '1969', '1968', '1967',
            '1966', '1965', '1964', '1963', '1962', '1961', '1960']

    for year in list_of_years:
        if data.get(year):
                return year, data.get(year)
    return None, None

if __name__ == '__main__':
    main()

