from datetime import datetime
from random import choices

from flask import url_for

from . import db
from .exceptions import (IncorrectOriginalException, IncorrectShortException,
                         NonUniqueException)
from settings import (ORIGINAL_LINK_LENGTH, REDIRECT_VIEW, SHORT_LENGTH,
                      SHORT_REGEX, SHORT_SIZE, SYMBOLS)

NAME_ALREADY_EXISTS = 'Имя "{}" уже занято.'
INCORRECT_NAME_SHORT_URL = 'Указано недопустимое имя для короткой ссылки'
INCORRECT_SYMBOLS = 'Используется некорректные символы'
CANT_GENERATE = 'Не удалось сгенерировать короткий идентификатор'
SYMBOLS_LIMIT = '{} ссылка превысила лимит количества символов'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text(ORIGINAL_LINK_LENGTH), nullable=False)
    short = db.Column(db.String(SHORT_LENGTH), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                REDIRECT_VIEW,
                short=self.short,
                _external=True
            )
        )

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_or_404(short):
        return URLMap.query.filter_by(short=short).first_or_404().original

    @staticmethod
    def create_short():
        for _ in range(SHORT_SIZE):
            short = ''.join((choices(SYMBOLS, k=SHORT_SIZE)))
            if not URLMap.get(short):
                return short
        raise IncorrectShortException(CANT_GENERATE)

    @staticmethod
    def create(original, short=None, is_validate=True):
        if is_validate:
            if len(original) > ORIGINAL_LINK_LENGTH:
                raise IncorrectOriginalException(
                    SYMBOLS_LIMIT.format('Оригинальная')
                )
            if short:
                if len(short) > SHORT_LENGTH:
                    raise IncorrectShortException(
                        SYMBOLS_LIMIT.format('Короткая')
                    )
                if not SHORT_REGEX.match(short):
                    raise IncorrectShortException(INCORRECT_SYMBOLS)
                if URLMap.get(short):
                    raise NonUniqueException(
                        NAME_ALREADY_EXISTS.format(short)
                    )
        url_map = URLMap(
            original=original,
            short=short or URLMap.create_short()
        )
        db.session.add(url_map)
        db.session.commit()
        return url_map
