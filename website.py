#!/usr/bin/env python
import csv
from decimal import Decimal
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form, TextField, DecimalField, SelectField, Required


# Create an app and configure it
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('settings.py')
app.config.from_pyfile('local.py', silent=True)
db = SQLAlchemy(app)


# Model
class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String(3), unique=True)
    country_name = db.Column(db.String(80), unique=True)
    year = db.Column(db.Integer())
    ppp = db.Column(db.Numeric(2))

    def __repr__(self):
        return '<Country %s>' % self.country_name


# Form
class SalaryForm(Form):
    from_country = SelectField(u'Which origin country do you want to compare from?', coerce=int)
    salary = DecimalField(u"Salary in origin country's local currency", validators=[Required()])
    to_country = SelectField(u'Which country do you want to compare with?', coerce=int)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SalaryForm()
    currency_value=None
    tocountry=None
    form.from_country.choices = [(country.id, country.country_name) for country in Country.query.order_by('country_name').all()]
    form.to_country.choices = [(country.id, country.country_name) for country in Country.query.order_by('country_name').all()]
    if form.validate_on_submit():
        fromcountry = Country.query.get(form.from_country.data)
        tocountry = Country.query.get(form.to_country.data)
        if fromcountry or tocountry is not None:
            currency_value = moneyfmt((form.salary.data / fromcountry.ppp) * tocountry.ppp)
    return render_template('index.html', form=form, currency_value=currency_value, home=True, tocountry=tocountry)


@app.route('/json')
def jsondata():
    countries = Country.query.all()
    return jsonify({'countries': countries})


@app.route('/about')
def about():
    return render_template('about.html', about=True)


@app.route('/data')
def data():
    return render_template('data.html', data=True)


@app.route('/contact')
def contact():
    return render_template('contact.html', contact=True)


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
    digits = map(str, digits)
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

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
