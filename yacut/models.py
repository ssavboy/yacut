from datetime import datetime
from random import choices

from flask import url_for

from settings import (CUSTOM_ID_LENGTH, CUSTOM_ID_REGEX, ORIGINAL_LINK_LENGTH,
                      REDIRECT_VIEW, SHORT_SIZE, SYMBOLS)

from . import db
from .exceptions import IncorrectShortException, NonUniqueException

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
    def validate_short(short):
        if len(short) > CUSTOM_ID_LENGTH:
            raise IncorrectShortException()
        if not CUSTOM_ID_REGEX.findall(short):
            raise IncorrectShortException()
        return short

    @staticmethod
    def is_unique(short):
        return not URLMap.query.filter_by(short=short).first()

    @staticmethod
    def create_short():
        short = ''.join((choices(SYMBOLS, k=SHORT_SIZE)))
        if not URLMap.is_unique(short):
            URLMap.create_short()
        return short

    @staticmethod
    def create(original, short=None):

        if short:
            short = URLMap.validate_short(short)
            if not URLMap.is_unique(short):
                raise NonUniqueException()
        url = URLMap(
            original=original,
            short=short or URLMap.create_short()
        )
        db.session.add(url)
        db.session.commit()
        return url
