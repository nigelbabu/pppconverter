#!/usr/bin/env python
from decimal import Decimal
from flask import Flask, render_template, jsonify, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import DecimalField, SelectField
from wtforms.validators import InputRequired


# Create an app and configure it
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('settings.py')
app.config.from_pyfile('local.py', silent=True)
db = SQLAlchemy(app)


# Model
class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code3 = db.Column(db.String(3), unique=True)
    name = db.Column(db.String(80), unique=True)
    year = db.Column(db.Integer())
    ppp = db.Column(db.Numeric(2))

    def __repr__(self):
        return '<Country {0}>'.format(self.name)


class Config(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(80), unique=True)
    value = db.Column(db.String(80))

    def __repr__(self):
        return '<Config {0}: {1}>'.format(self.key, self.value)


# Form
class SalaryForm(Form):
    from_country = SelectField('Source country' , coerce=int)
    salary = DecimalField("Amount in source country's local currency",
                          validators=[InputRequired()])
    to_country = SelectField('Target country', coerce=int)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SalaryForm()
    currency_value = None
    tocountry = None
    form.from_country.choices = [(country.id, country.name) for country in
                                 Country.query.order_by('name').all()]
    form.to_country.choices = [(country.id, country.name) for country in
                               Country.query.order_by('name').all()]
    if form.validate_on_submit():
        fromcountry = Country.query.get(form.from_country.data)
        tocountry = Country.query.get(form.to_country.data)
        if fromcountry or tocountry is not None:
            currency_value = moneyfmt((form.salary.data / fromcountry.ppp)
                                      * tocountry.ppp)
    conversion = Config.query.filter_by(key='gbp_rate').first()
    d = {
        'form': form,
        'currency_value': currency_value,
        'home': True,
        'tocountry': tocountry,
        'conversion_rate': float(conversion.value) * 100,
    }
    return render_template('index.html', **d)


@app.route('/json')
def jsondata():
    countries = Country.query.all()
    countrieslist = [{'id': country.id, 'name': country.name, 'ppp': str(country.ppp), 'code3': country.code3} for country in countries]
    return jsonify({'countries': countrieslist})


@app.route('/about')
@app.route('/data')
@app.route('/contact')
def archived_paths():
    return redirect('/', code=301)


def moneyfmt(value, places=2, curr='', sep=',', dp='.',
             pos='', neg='-', trailneg=''):
    """Convert Decimal to a money formatted string.

    places:  required number of places after the decimal point
    curr:    optional currency symbol before the sign (may be blank)
    sep:     optional grouping separator (comma, period, space, or blank)
    dp:      decimal point indicator (comma or period)
             only specify as blank when places is zero
    pos:     optional sign for positive numbers: '+', space or blank
    neg:     optional sign for negative numbers: '-', '(', space or blank
    trailneg:optional trailing minus indicator:  '-', ')', space or blank

    >>> d = Decimal('-1234567.8901')
    >>> moneyfmt(d, curr='$')
    '-$1,234,567.89'
    >>> moneyfmt(d, places=0, sep='.', dp='', neg='', trailneg='-')
    '1.234.568-'
    >>> moneyfmt(d, curr='$', neg='(', trailneg=')')
    '($1,234,567.89)'
    >>> moneyfmt(Decimal(123456789), sep=' ')
    '123 456 789.00'
    >>> moneyfmt(Decimal('-0.02'), neg='<', trailneg='>')
    '<0.02>'

    """
    q = Decimal(10) ** -places      # 2 places --> '0.01'
    sign, digits, exp = value.quantize(q).as_tuple()
    result = []
    digits = list(map(str, digits))
    build, next = result.append, digits.pop
    if sign:
        build(trailneg)
    for i in range(places):
        build(next() if digits else '0')
    build(dp)
    if not digits:
        build('0')
    i = 0
    while digits:
        build(next())
        i += 1
        if i == 3 and digits:
            i = 0
            build(sep)
    build(curr)
    build(neg if sign else pos)
    return ''.join(reversed(result))
