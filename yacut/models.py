from datetime import datetime
from random import choice
from re import match

from flask import url_for

from settings import redirect_view, symbols

from . import db
from .const import (CUSTOM_ID_LENGTH, CUSTOM_ID_REGEX, ORIGINAL_LINK_LENGTH,
                    SHORT_ID_LENGTH)
from .error_handlers import InvalidAPIUsageError

NAME_ALREADY_EXISTS = 'Имя "{}" уже занято.'
INCORRECT_NAME_SHORT_URL = 'Указано недопустимое имя для короткой ссылки'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text(ORIGINAL_LINK_LENGTH), nullable=False)
    short = db.Column(db.String(CUSTOM_ID_LENGTH), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                redirect_view,
                short=self.short,
                _external=True
            )
        )

    @staticmethod
    def get_short(custom_id):
        return URLMap.query.filter_by(short=custom_id).first()

    @staticmethod
    def get_short_or_404(short):
        return URLMap.query.filter_by(short=short).first_or_404().original

    @staticmethod
    def get_unique_short_id():
        return ''.join((choice(symbols) for _ in range(SHORT_ID_LENGTH)))

    @staticmethod
    def check_uniqueness_short_id(custom_id):
        if not URLMap.get_short(custom_id):
            return None
        return custom_id

    @staticmethod
    def micro_orm(data, custom_id):

        if 'custom_id' not in data or custom_id is None:
            data['custom_id'] = URLMap.get_unique_short_id()
        if custom_id:
            if URLMap.get_short(custom_id) is not None:
                raise InvalidAPIUsageError(NAME_ALREADY_EXISTS.format(custom_id))
            if not match(CUSTOM_ID_REGEX, custom_id) or len(custom_id) > CUSTOM_ID_LENGTH:
                raise InvalidAPIUsageError(INCORRECT_NAME_SHORT_URL)
        url_map = URLMap(
            original=data['url'],
            short=data['custom_id']
        )
        db.session.add(url_map)
        db.session.commit()
        return url_map
