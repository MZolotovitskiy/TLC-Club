from flask import Flask, render_template

# HTML шаблон слетает из-за комментариев поэтому напишу здесь.  На место # поставить относительный адресс войти потом поменять на jinja if
# Специальный комментарий для Валентина Я не буду убирать закругление углов с фотки крузака, что-то не нравится - убери её и сделай домашнюю страницу как на нормальных сайтах
# Блок контент и эндблок добавите сами

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


def main():
    app.run()


if __name__ == '__main__':
    main()
