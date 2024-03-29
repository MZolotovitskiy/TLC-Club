from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class TownForm(FlaskForm):
    town = StringField('Город', validators=[DataRequired()])
    submit = SubmitField('Найти')

