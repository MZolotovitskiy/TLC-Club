import os
import datetime as dt
import random
from flask import Flask, render_template, redirect
from data.services_town_ask import TownForm
from functions import search

app = Flask(__name__)
secret_key = "%032x" % random.getrandbits(128)
app.config['SECRET_KEY'] = secret_key

TEARDOWN_COUNTER = 0


@app.route('/services', methods=['GET', 'POST'])
def services_ask():
    form = TownForm()
    if form.validate_on_submit():
        # print(form.town.data)
        return redirect(f'/services/{form.town.data}')
    return render_template('services_ask.html', title='Введите город', form=form)


@app.route('/services/<town>')
def services(town):
    services = search.search(town)
    title = f'Сервисы в городе {town.capitalize()}'
    return render_template('services.html', title=title, services=services)


@app.after_request
def after_request(response):
    for currentdir, dirs, files in os.walk('static/cash'):
        for k in files:
            create_data = dt.datetime.fromtimestamp(os.path.getctime('static/cash/' + k))
            a = dt.datetime.now() - create_data
            if a >= dt.timedelta(minutes=1):
                os.remove('static/cash/' + k)
    return response


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
