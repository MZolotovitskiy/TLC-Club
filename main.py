import os
import datetime as dt
import random
from flask import Flask, render_template, redirect, session, abort
from data import db_session
from data.users import User
from data.reviews import Review
from data.review_pictures import ReviewPicture
from data.threads import Thread
from data.messages import Message
from flask_login import LoginManager, login_user, current_user, login_required
from forms.user import RegisterForm, FinishRegistrationForm, LoginForm
from mailer import send_email, EMailText
from forms.services_town_ask import TownForm
from forms.forum import ThreadForm, MessageForm
from forms.reviews import ReviewForm
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
    if current_user.is_authenticated:
        if user_id == current_user.id:
            return redirect('/my_account')
    elif user:
        return render_template('account.html', title=f'Аккаунт {user.username}', user=user)
    else:
        abort(404)


@app.route('/my_account')
@login_required
def my_account():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        user = db_sess.get(User, current_user.id)  # Данная строчка может показаться бессмысленной, но
        # если передать current_user будет ошибка
        return render_template('account.html', title=f'Аккаунт {user.username}', user=user, personal=True)
    else:
        abort(401)


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


@app.route('/reviews_delete/<int:id>')
@login_required
def reviews_delete(id):
    db_sess = db_session.create_session()
    review = db_sess.get(Review, int(id))
    if review:
        db_sess.delete(review)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/my_account')


@app.route('/forum/delete/<int:id>')
@login_required
def threads_delete(id):
    db_sess = db_session.create_session()
    thread = db_sess.get(Thread, int(id))
    if thread:
        for message in thread.messages:
            db_sess.delete(message)
        db_sess.delete(thread)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/my_account')


@app.route('/reviews/create_review', methods=['GET', 'POST'])
def create_review():
    form = ReviewForm()
    if not current_user.is_authenticated:
        abort(401)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        review = Review()
        review.author_id, review.title, review.content, review.preview = current_user.id, form.title.data, \
            form.content.data, base64.b64encode(form.preview.data.read()).decode('ascii')
        db_sess.add(review)
        db_sess.commit()
        db_sess.flush()
        review_id = review.id
        for file in form.media.data:
            picture = ReviewPicture()
            picture.review_id, picture.bytes = review_id, base64.b64encode(file.read()).decode('ascii')
            db_sess.add(picture)
        db_sess.commit()
        return redirect('/reviews')
    return render_template('create_review.html', title='Написание Обзора', form=form)


@app.route('/reviews')
def reviews():
    db_sess = db_sess = db_session.create_session()
    reviews = []
    for review in db_sess.query(Review):
        reviews.append(review)
    return render_template('reviews.html', title='Обзоры', reviews=reviews)


@app.route('/reviews/<int:id>')
def review(id):
    db_sess = db_sess = db_session.create_session()
    review = db_sess.get(Review, int(id))
    if review:
        return render_template('review_view.html', title=review.title, review=review)
    else:
        abort(404)


@app.route('/forum/edit/<int:thread_id>', methods=['GET', 'POST'])
@login_required
def change_thread(thread_id):
    form = ThreadForm()
    db_sess = db_sess = db_session.create_session()
    thread = db_sess.get(Thread, int(thread_id))
    if thread:
        if current_user.is_authenticated:
            if current_user.id == thread.author.id:
                if form.validate_on_submit():
                    thread.title = form.title.data
                    if form.media.data:
                        thread.picture = base64.b64encode(form.media.data.read()).decode('ascii')
                    thread.content = form.content.data
                    db_sess.commit()
                    return redirect('/forum')
                else:
                    form.title.data = thread.title
                    form.content.data = thread.content
                    return render_template('create_thread.html', title='Редактирование Треда', form=form)
            else:
                abort(403)
        else:
            abort(401)
    else:
        abort(404)


@app.route('/reviews/edit/<int:review_id>', methods=['GET', 'POST'])
@login_required
def change_review(review_id):
    form = ReviewForm()
    db_sess = db_sess = db_session.create_session()
    review = db_sess.get(Review, int(review_id))
    if review:
        if current_user.is_authenticated:
            if current_user.id == review.author.id:
                if form.validate_on_submit():
                    review.title = form.title.data
                    if form.preview.data:
                        review.preview = base64.b64encode(form.preview.data.read()).decode('ascii')
                    if form.media.data:
                        for file in form.media.data:
                            picture = ReviewPicture()
                            picture.review_id, picture.bytes = review.id, base64.b64encode(file.read()).decode('ascii')
                            db_sess.add(picture)
                    review.content = form.content.data
                    db_sess.commit()
                    return redirect('/reviews')
                else:
                    form.title.data = review.title
                    form.content.data = review.content
                    return render_template('create_review.html', title='Редактирование Обзора', form=form)
            else:
                abort(403)
        else:
            abort(401)
    else:
        abort(404)


@app.route('/news')
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(News)
    # .filter(News.is_private != True) - возможности для улучшения
    return render_template("show_news.html", news=news)


@app.route('/news', methods=['GET', 'POST'])
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('news.html', title='Добавление новости',
                           form=form)


@app.route('/news/<int:id>', methods=['GET', 'POST'])
def edit_news(id):
    form = NewsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('news.html',
                           title='Редактирование новости',
                           form=form
                           )


@app.route('/photos', methods=['GET'])
def photos():
    db_sess = db_session.create_session()
    sp, model = [], db_sess.query(photos).first().model
    for url in db_sess.query(photos).all():
        sp.append(url.url)
    return render_template('photos.html', title=model, photos=sp)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, int(user_id))


def main():
    db_session.global_init("db/TLC_db.db")
    app.run()


if __name__ == '__main__':
    main()
