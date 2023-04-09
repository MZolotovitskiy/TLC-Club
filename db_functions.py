from data import db_session
from data.users import User


def check_available(username, login, email):
    # Функция проверяющая доступность имени пользователя, почты и логина при регистрации.
    # При вызове получает значения и возвращает картеж из трёх булевых переменных.
    db_sess = db_session.create_session()
    us_av, log_av, em_av = True, True, True
    for user in db_sess.query(User).all():
        if user.username == username:
            us_av = False
            break
        if user.login == login:
            log_av = False
            break
        if user.email == email:
            em_av = False
            break
    return us_av, log_av, em_av


def add_user(username, login, email, password):
    user = User(
        username=username,
        login=login,
        email=email
    )
    db_sess = db_session.create_session()
    user.set_password(password)
    db_sess.add(user)
    db_sess.commit()
    return True # Возвращает значение True в случае успеха
