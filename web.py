import os
import random
import time
import flask.wrappers
import requests
from flask import Flask, render_template, redirect
from data.services_town_ask import TownForm
from functions import search
import asyncio
import schedule

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


# @app.teardown_request
# def add_header(response):
#     global TEARDOWN_COUNTER
#     TEARDOWN_COUNTER += 1
#     if TEARDOWN_COUNTER % 4 == 0 and TEARDOWN_COUNTER != 0:
#         for currentdir, dirs, files in os.walk('static/hash'):
#             for k in files:
#                 os.remove(currentdir + '/' + k)
#         print(123)
#
#     print(TEARDOWN_COUNTER)
#     return response

# @app.after_request
# def aaa_help_pls(response):
#     if response.is_streamed:
#         time.sleep(5)
#         # photo = list(response.iter_encoded())[0]
#         for currentdir, dirs, files in os.walk('static/cash'):
#             for k in files:
#                 print(k)
#                 # with open(currentdir + '/' + k, mode='rb') as file:
#                 #     # if file == photo:
#                 os.remove(currentdir + '/' + k)
#     print(response)
#     return response


# def cash_delete():
#     print(123)


#
#
# async def await_func():
#     await asyncio.gather(asyncio.create_task(cash_delete()))

# schedule.every(1).seconds.do(cash_delete)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        app.run(port=8080, host='127.0.0.1')
    # if os.name == 'nt':
    #     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    #
    # asyncio.run(await_func())

