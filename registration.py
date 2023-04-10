from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from data.jobs import Jobs
from forms.user import RegisterForm, FinishRegistrationForm, LoginForm
from mailer import send_email, EMailText
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)

# from flask_login import LoginManager, login_user, login_required, logout_user, current_user
#
# login_manager = LoginManager()
# login_manager.init_app(app)


# Крч ятакпон, что эти штуки нужны для всяких приколов, что ты залогинен на сайте.

def main():
    # db_session.global_init("db/mars.db") # Тут тож допиши че нить
    app.run()


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            print("Пароли не совпадают")
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        # db_sess = db_session.create_session()                                 # Тут надо БД подключать!!!
        # if db_sess.query(User).filter(User.email == form.email.data).first():
        #     print("Такой пользователь уже есть")
        #     return render_template('register.html', title='Регистрация',
        #                            form=form,
        #                            message="Такой пользователь уже есть")
        user = User(
            login=form.login.data,
            username=form.username.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        text, code = EMailText().registration()
        send_email(user.email, 'Завершите регистрацию', text)
        return redirect('/finish_registration')
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/finish_registration", methods=['GET', 'POST'])
def finish_registration():
    form = FinishRegistrationForm()
    if form.validate_on_submit():
        pass
        # Миша, продолжи!

        # Тут надо сопоставить код и почту из предыдущей функции с тем, что передались в новенькую форму.

        return redirect('/login')
    return render_template('finishregistration.html', title='Закончите регистрацию', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        redirect('/')
    return render_template('login.html', title='Вход', form=form)


if __name__ == '__main__':
    main()
