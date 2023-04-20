from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField, TextAreaField, MultipleFileField
from wtforms.validators import DataRequired, Optional
from flask_wtf.file import FileAllowed


class ReviewForm(FlaskForm):
    title = StringField('Тема', validators=[DataRequired()])
    content = TextAreaField('Текст', validators=[DataRequired()])
    preview = FileField('Превью', validators=[DataRequired(), FileAllowed(['jpg', 'png'])])
    media = MultipleFileField('Изображения', validators=[Optional(), FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Создать')
