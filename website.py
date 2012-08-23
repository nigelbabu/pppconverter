#!/usr/bin/env python
import csv
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form, TextField, DecimalField, SelectField, Required


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
    from_country = SelectField(u'Country of Origin', coerce=unicode)
    salary = DecimalField(u'Salary in local currency', validators=[Required()])
    to_country = SelectField(u'Destination Country', coerce=unicode)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SalaryForm()
    form.from_country.choices = ((country.country_code, country.country_name) for country in Country.query.all())
    form.to_country.choices = ((country.country_code, country.country_name) for country in Country.query.all())
    currency_value = None
    if form.validate_on_submit():
        from_country = Country.query.filter_by(country_code=form.from_country.data).first()
        to_country = Country.query.filter_by(country_code=form.to_country.data).first()
        if from_country or to_country is not None:
            currency_value = (float(form.salary.data) / float(from_country.ppp)) * to_country.ppp
    return render_template('index.html', form=form, currency_value=currency_value)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
