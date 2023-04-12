from flask import Flask, render_template, redirect
# from data import db_session
from data.users import User
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
    # Ниже будет User для теста
    u = User
    u.username = 'Sirenogoloviy'
    u.email = 's.tiktok-trend@podkraduli.ru'
    # тут крч должен быть поиск в бд по id юзера всяких там сообщений и тд ну ты пон

    return render_template('account.html', title=f'Аккаунт {u.username}', user=u)


main()