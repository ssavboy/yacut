from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp

from .const import PATTERN


class URLForm(FlaskForm):
    original_link = URLField(
        'Поле для оригинальной ссылки',
        validators=[
            DataRequired('Обязательное поле для заполнения'),
            URL(message='Некорректная ссылка')
        ]
    )
    custom_id = URLField(
        'Поле для короткого идентификатора',
        validators=[
            Optional(),
            Length(1, 6),
            Regexp(
                regex=PATTERN,
                message='Некорректные символы: только латинские буквы и цифры'
            )
        ]
    )
    submit = SubmitField('Создать')
