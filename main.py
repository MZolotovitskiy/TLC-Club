import os
import datetime as dt
import random
from flask import Flask, render_template, redirect, session, abort
from data import db_session
from data.users import User
from data.reviews import Review
from data.threads import Thread
from data.messages import Message
from flask_login import LoginManager, login_user, current_user
from forms.user import RegisterForm, FinishRegistrationForm, LoginForm
from mailer import send_email, EMailText
from forms.services_town_ask import TownForm
from forms.forum import ThreadForm, MessageForm
from functions import search
import base64

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


@app.route('/account/<int:user_id>')
def account(user_id):
    db_sess = db_session.create_session()
    user = db_sess.get(User, int(user_id))
    if user:
        reviews, threads = [], []
        for review in db_sess.query(Review).filter(Review.author_id == user_id):
            reviews.append(review)
        for thread in db_sess.query(Thread).filter(Thread.author_id == user_id):
            threads.append(thread)
        return render_template('account.html', title=f'Аккаунт {user.username}',
                               user=user, reviews=reviews, threads=threads)
    else:
        abort(404)


@app.route('/forum/create_thread', methods=['GET', 'POST'])
def create_thread():
    form = ThreadForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        thread = Thread()
        thread.title, thread.content = form.title.data, form.content.data
        thread.picture = base64.b64encode(form.media.data.read()).decode('ascii')
        if current_user.is_authenticated:
            thread.author_id = current_user.id
        db_sess.add(thread)
        db_sess.commit()
        return redirect('/forum')
    return render_template('create_thread.html', title='Создание Треда', form=form)


@app.route('/forum')
def forum():
    db_sess = db_sess = db_session.create_session()
    threads = []
    pictures = {}
    for thread in db_sess.query(Thread):
        threads.append(thread)
    return render_template('forum.html', title='Форум', threads=threads)


@app.route('/forum/<int:thread_id>')
def thread_view(thread_id):
    db_sess = db_sess = db_session.create_session()
    thread = db_sess.get(Thread, int(thread_id))
    if thread:
        return render_template('thread_view.html', title=thread.title, thread=thread)
    else:
        abort(404)


@app.route('/forum/write_message/<int:thread_id>', methods=['GET', 'POST'])
def write_message(thread_id):
    form = MessageForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        thread = db_sess.get(Thread, int(thread_id))
        if thread:
            message = Message()
            message.content, message.thread_id = form.content.data, thread_id
            if form.media:
                message.picture = base64.b64encode(form.media.data.read()).decode('ascii')
            if current_user.is_authenticated:
                message.author_id = current_user.id
            db_sess.add(message)
            db_sess.commit()
            return redirect(f'/forum/{thread_id}')
        else:
            abort(404)
    return render_template('create_message.html', title='Написание сообщения', form=form)


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
