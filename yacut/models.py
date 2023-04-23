from datetime import datetime
from random import choices

from flask import url_for

from settings import (CUSTOM_ID_LENGTH, ORIGINAL_LINK_LENGTH, REDIRECT_VIEW,
                      SYMBOLS)

from . import db
from .exceptions import (IncorrectOriginalException, IncorrectShortException,
                         NonUniqueException)

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
    def get_short(custom_id):
        return URLMap.query.filter_by(short=custom_id).first()

    @staticmethod
    def get_or_404(short):
        return URLMap.query.filter_by(short=short).first_or_404().original

    @staticmethod
    def create_id():
        return ''.join((choices(SYMBOLS, k=6)))

    @staticmethod
    def validate_short(short):
        if len(short) > CUSTOM_ID_LENGTH:
            return False
        for char in short:
            if char not in SYMBOLS:
                return False
        return True

    @staticmethod
    def is_unique(short):
        return not URLMap.query.filter_by(short=short).first()

    @staticmethod
    def create_url_object(original, short=None):
        if len(original) > ORIGINAL_LINK_LENGTH:
            raise IncorrectOriginalException
        if short:
            if not URLMap.validate_short(short):
                raise IncorrectShortException()
            if not URLMap.is_unique(short):
                raise NonUniqueException()
        url = URLMap(
            original=original,
            short=short or URLMap.create_id()
        )
        db.session.add(url)
        db.session.commit()
        return url
