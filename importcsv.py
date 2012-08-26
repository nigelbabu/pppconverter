#!/usr/bin/env python
from website import Country, db
import csv

ppp_data = csv.reader(open('data.csv'))
for line in ppp_data:
    country = Country(name=line[0], code3=line[1], year=line[2], ppp=line[3])
    db.session.add(country)
    db.session.commit()
