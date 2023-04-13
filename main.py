from flask import Flask, render_template, redirect, abort
from data import db_session
from data.users import User
from data.reviews import Review
from data.threads import Thread
from data.messages import Message
from mailer import send_email, EMailText
import datetime
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)


# login_manager = LoginManager()
# login_manager.init_app(app)


def main():
    # db_session.global_init("db/mars.db") # Тут тож допиши че нить
    app.run()


@app.route('/account/<int:userid>')
def account(userid):
    # Тут крч должен быть запрос в БД с поиском юзера с указанным ID

    # потом крч если нету юзера то надо вернуть 404

    # Ниже будет User для теста
    u = User()
    u.username = 'Sirenogoloviy'
    u.email = 's.tiktok-trend@podkraduli.ru'
    # тут крч должен быть поиск в бд по id юзера всяких там сообщений и тд ну ты пон

    reviews = dict()

    r1 = Review()
    r1.title = 'Обзор на новый звуковой сигнал'
    r1_url = 'r1'
    reviews[r1] = r1_url

    print(reviews)

    r2 = Review()
    r2.title = 'Обзор на новую акустику'
    r2_url = 'r2'
    reviews[r2] = r2_url

    print(reviews, r1)

    # reviews = dict()

    threads = dict()

    # ну крч тут про треды такая же система

    # я так подумал и сообщения не будем сюда писать типо зачем лол

    return render_template('account.html', title=f'Аккаунт {u.username}', user=u, reviews=reviews, threads=threads)


@app.route('/myaccount')
def myaccount():
    abort(503)


main()
