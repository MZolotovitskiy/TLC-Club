import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class ReviewPicture(SqlAlchemyBase):
    __tablename__ = 'review_pictures'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    review_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("reviews.id"))
    bytes = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)
    review = orm.relationship('Review')
