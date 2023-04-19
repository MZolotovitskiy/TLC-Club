from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional
from flask_wtf.file import FileAllowed


class ThreadForm(FlaskForm):
    title = StringField('Тема', validators=[DataRequired()])
    media = FileField('Изображение', validators=[Optional(), FileAllowed(['jpg', 'png'])])
    content = TextAreaField('Текст', validators=[DataRequired()])
    submit = SubmitField('Создать')


class MessageForm(FlaskForm):
    media = FileField('Изображение', validators=[Optional(), FileAllowed(['jpg', 'png'])])
    content = TextAreaField('Текст', validators=[DataRequired()])
    submit = SubmitField('Создать')
