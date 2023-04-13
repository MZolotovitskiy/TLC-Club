import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Thread(SqlAlchemyBase):
    __tablename__ = 'threads'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    messages = orm.relationship("Message", back_populates='thread')
    # возможности для дальнейшей модификации
    # created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    #  is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
