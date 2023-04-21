from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp

from .const import CUSTOM_ID_LENGTH, CUSTOM_ID_REGEX, ORIGINAL_LINK_LENGTH


class URLForm(FlaskForm):
    original_link = URLField(
        'Поле для оригинальной ссылки',
        validators=[
            DataRequired('Обязательное поле для заполнения'),
            URL(message='Некорректная ссылка'),
            Length(max=ORIGINAL_LINK_LENGTH)
        ]
    )
    custom_id = URLField(
        'Поле для короткого идентификатора',
        validators=[
            Optional(),
            Length(max=CUSTOM_ID_LENGTH),
            Regexp(
                regex=CUSTOM_ID_REGEX,
                message='Некорректные символы: только латинские буквы и цифры'
            )
        ]
    )
    submit = SubmitField('Создать')
