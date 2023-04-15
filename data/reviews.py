import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Review(SqlAlchemyBase):
    __tablename__ = 'reviews'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    # возможности для дальнейшей модификации
    # created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    #  is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
