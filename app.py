from flask import Flask, render_template, flash, request
from flask_table import Table, Col, ButtonCol
from wtforms import Form, IntegerField, TextField, validators

import database

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


class TimeCol(Col):
    def td_format(self, content):
        return int(content)/60


class CounterTable(Table):
    user = Col('User')
    seconds = TimeCol('Minutes')


class AdminTable(CounterTable):
    add = ButtonCol('Topup', 'topup', url_kwargs=dict(user='user'))


class Counter(object):
    def __init__(self, user, seconds):
        self.user = user
        self.seconds = seconds / 60


class ReusableForm(Form):
    minutes = IntegerField('Minutes:', validators=[validators.required()])

@app.route("/zabla/")
def zabla():
    db = database.Database()
    items = db.counters.all()
    table = CounterTable(items)
    return table.__html__()


@app.route("/zabla/admin/")
def admin():
    db = database.Database()
    items = db.counters.all()
    table = AdminTable(items)
    return table.__html__()


@app.route("/zabla/topup/<string:user>", methods=['GET', 'POST'])
def topup(user):
    form = ReusableForm(request.form)

    if request.method == 'POST':
        minutes = request.form['minutes']
        if form.validate():
            flash('Added ' + minutes + ' minutes')
        else:
            flash('Error: missing value for minutes ')

    return render_template('topup.html', form=form, user=user)


@app.errorhandler(404)
def page_not_found(error):
    return 'Sorry, no more minutes left :-('


if __name__ == "__main__":
    app.run()
