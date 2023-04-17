from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp, URL


class URLForm(FlaskForm):
    original_link = URLField(
        'Поле для оригинальной ссылки',
        validators=[
            DataRequired('Обязательное поле для заполнения'),
            URL(message='Некорректный url')
        ]
    )
    custom_id = URLField(
        'Поле для короткого идентификатора',
        validators=[
            Optional(),
            Length(6),
            Regexp(
                regex=r'^[a-zA-z\d]{1,16}$',
                message='Некорректные символы: только латинские буквы и цифры'
            )
        ]
    )
    submit = SubmitField('Создать')
