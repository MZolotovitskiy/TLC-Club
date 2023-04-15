import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Thread(SqlAlchemyBase):
    __tablename__ = 'threads'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    date_of_creation = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    is_open = sqlalchemy.Column(sqlalchemy.BOOLEAN, default=True)
    messages = orm.relationship("Message", back_populates='thread')
