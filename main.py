import os
import datetime as dt
import random
from flask import Flask, render_template, redirect, session
from data import db_session
from data.users import User
from data.reviews import Review
from data.threads import Thread
from data.messages import Message
from flask_login import LoginManager, login_user
from forms.user import RegisterForm, FinishRegistrationForm, LoginForm
from mailer import send_email, EMailText
from forms.services_town_ask import TownForm
from functions import search

app = Flask(__name__)
app.config['SECRET_KEY'] = "%032x" % random.getrandbits(128)
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', title='Главная')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form, message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже существует")
        text, code = EMailText().registration()
        new_user = {'username': form.username.data, 'email': form.email.data,
                    'password': form.password.data, 'code': code}
        session['user'] = new_user
        send_email(form.email.data, 'Завершите регистрацию', text)
        return redirect('/finish_registration')
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/finish_registration", methods=['GET', 'POST'])
def finish_registration():
    form = FinishRegistrationForm()
    if form.validate_on_submit():
        new_user = session['user']
        if str(form.code.data) == new_user['code'] and form.email.data == new_user['email']:
            user = User()
            user.username, user.email = new_user['username'], new_user['email']
            user.set_password(new_user['password'])
            db_sess = db_session.create_session()
            db_sess.add(user)
            db_sess.commit()
            session.pop('user', None)
            return redirect('/login')
        else:
            return render_template('login.html', title='Вход', form=form,
                                   message='Неверный код, или email. Попробуйте ещё раз.')
    return render_template('finish_registration.html', title='Завершите регистрацию', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter((User.email == form.email.data)).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/home')
        else:
            return render_template('login.html', itle='Вход', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Вход', form=form)


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


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, int(user_id))


@app.route('/myaccount')
def myaccount():
    abort(503)


def main():
    db_session.global_init("db/TLC_db.db")
    app.run()


if __name__ == '__main__':
    main()
