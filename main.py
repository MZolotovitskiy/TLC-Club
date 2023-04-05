from flask import Flask, render_template
from data import db_session

# Данные для входа с целью отладки/проверки
# user: Test User
# password: testuser2281337
# (НА ДАННОМ ЭТАПЕ РАЗРАБОТКИ НЕ РАБОТАЕТ)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


def main():
    db_session.global_init("db/TLC_db.db")
    app.run()


if __name__ == '__main__':
    main()
