from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import (URL, DataRequired, Length, Optional, Regexp,
                                ValidationError)

from .models import URLMap
from settings import ORIGINAL_LINK_LENGTH, SHORT_LENGTH, SHORT_REGEX

ALREADY_TAKEN = 'Имя {} уже занято!'
FIELD_ORIGINAL_LINK = 'Поле для оригинальной ссылки'
FIELD_SHORT_ID = 'Поле для короткого идентификатора'
REQUIRED_FIELD = 'Обязательное поле для заполнения'
INCORRECT_ORIGINAL_LINK = 'Некорректная ссылка'
INCORRECT_SHORT_LINK = 'Некорректные символы: только латинские буквы и цифры'
CREATE = 'Создать'


class URLForm(FlaskForm):
    original_link = URLField(
        FIELD_ORIGINAL_LINK,
        validators=[
            DataRequired(REQUIRED_FIELD),
            URL(message=INCORRECT_ORIGINAL_LINK),
            Length(max=ORIGINAL_LINK_LENGTH)
        ]
    )
    custom_id = URLField(
        FIELD_SHORT_ID,
        validators=[
            Optional(),
            Length(max=SHORT_LENGTH),
            Regexp(
                regex=SHORT_REGEX,
                message=INCORRECT_SHORT_LINK
            )
        ]
    )
    submit = SubmitField(CREATE)

    def validate_custom_id(self, field):
        if URLMap.get(field.data):
            raise ValidationError(ALREADY_TAKEN.format(field.data))
