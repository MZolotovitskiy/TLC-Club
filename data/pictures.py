import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Picture(SqlAlchemyBase):
    __tablename__ = 'pictures'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    route = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    thread_usage = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("threads.id"), nullable=True)
    message_usage = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("messages.id"), nullable=True)
    review_usage = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("reviews.id"), nullable=True)