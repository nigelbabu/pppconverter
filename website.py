#!/usr/bin/env python
import csv
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form, TextField, DecimalField, SelectField, Required
from baseframe import baseframe, baseframe_js, baseframe_css


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
    ppp = db.Column(db.Float(15))

    def __repr__(self):
        return '<Country %s>' % self.username


# Form
class SalaryForm(Form):
    from_country = SelectField(u'Where are you from?', coerce=int)
    salary = DecimalField(u'Salary in your local currency', validators=[Required()])
    to_country = SelectField(u'Where are you headed to?', coerce=int)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SalaryForm()
    currency_value=None
    form.from_country.choices = [(country.id, country.country_name) for country in Country.query.order_by('country_name').all()]
    form.to_country.choices = [(country.id, country.country_name) for country in Country.query.order_by('country_name').all()]
    if form.validate_on_submit():
        fromcountry = Country.query.get(form.from_country.data)
        tocountry = Country.query.get(form.to_country.data)
        if fromcountry or tocountry is not None:
            currency_value = (float(form.salary.data) / float(fromcountry.ppp)) * tocountry.ppp
    return render_template('index.html', form=form, currency_value=currency_value, home=True)


@app.route('/about')
def about():
    return render_template('about.html', about=True)


@app.route('/data')
def data():
    return render_template('data.html', data=True)


@app.route('/contact')
def contact():
    return render_template('contact.html', contact=True)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
