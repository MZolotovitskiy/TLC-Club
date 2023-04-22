import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class NewsPicture(SqlAlchemyBase):
    __tablename__ = 'news_pictures'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    review_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("news.id"))
    bytes = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    news = orm.relationship('News')
