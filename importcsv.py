#!/usr/bin/env python
from website import Country, db
import csv

ppp_data = csv.reader(open('data.csv'))
for line in ppp_data:
    country = Country(country_name=line[0], country_code=line[1], year=line[2], ppp=line[3])
    db.session.add(country)
    db.session.commit()
