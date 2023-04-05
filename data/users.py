import datetime
import sqlalchemy
# from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True) # index = ??
    login = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    username = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    # возможности для дальнейшей модификации
    # model = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # role = sqlalchemy.Column(sqlalchemy.String, nullable=False, default='user')
    # created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
