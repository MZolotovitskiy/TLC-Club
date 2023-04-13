from flask import Flask, render_template, redirect, session
from data import db_session
from data.users import User
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms.user import RegisterForm, FinishRegistrationForm, LoginForm
from mailer import send_email, EMailText

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


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
            return render_template('login.html',itle='Вход', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Вход', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, int(user_id))


def main():
    db_session.global_init("db/TLC_db.db")
    app.run()


if __name__ == '__main__':
    main()
