from flask import Flask, render_template
from flask_login import current_user
from data import db_session
from flask import redirect
from data.news import News
from forms.form_news import NewsForm
from requests import request
from os import abort

# Данные для входа с целью отладки/проверки
# user: Test User
# password: testuser2281337
# (НА ДАННОМ ЭТАПЕ РАЗРАБОТКИ НЕ РАБОТАЕТ)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


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


def main():
    db_session.global_init("db/TLC_db.db")
    app.run()


if __name__ == '__main__':
    main()
