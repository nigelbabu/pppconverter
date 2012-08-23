#!/usr/bin/env python
from lxml import etree
import csv

def remove_item(x, key):
    x.pop(key)
    return x

parsedxml = etree.parse('world_bank_ppp_data.xml')
data_writer = csv.writer(open('world_bank_pp_data.xml', 'wb'))
parsed_data = []
cleaned_data = {}
for record in parsedxml.iter('record'):
    row = []
    for field in record.iter('field'):
        row.append(field.text)
        if field.get('key'):
            row.append(field.get('key'))
    parsed_data.append(row)
parsed_data = map(lambda x: remove_item(x, 3), parsed_data)
parsed_data = map(lambda x: remove_item(x, 2), parsed_data)
parsed_data = filter(lambda x: x[3] is not None, parsed_data)
for item in parsed_data:
    cleaned_data[item[1]] = item
writer = csv.writer(open('data.csv', 'wb'))
for k, v in cleaned_data.iteritems():
    writer.writerow(v)
