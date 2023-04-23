from os import getenv
from re import compile, escape
from string import ascii_letters, digits

SHORT_SIZE = 6
CUSTOM_ID_LENGTH = 16
SYMBOLS = ascii_letters + digits
CUSTOM_ID_REGEX = compile('^[' + escape(SYMBOLS) + ']*$')
REDIRECT_VIEW = 'redirect_view'
ORIGINAL_LINK_LENGTH = 1000


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = getenv('SECRET_KEY')
